# functions to guess the gene model release given a list of gene IDs
# tested on python3 and python2
import logging, sys, optparse, string, glob, gzip, json, subprocess
from io import StringIO

from collections import defaultdict
from os.path import join, basename, dirname, isfile

from .cellbrowser import sepForFile, getStaticFile, openFile, splitOnce, setDebug, getStaticPath
from .cellbrowser import getGeneSymPath, downloadUrlLines, getSymToGene, getGeneBedPath, errAbort, iterItems
from .cellbrowser import findCbData, readGeneSymbols, getGeneJsonPath, getDownloadsUrl

# ==== functions =====
def cbGenes_parseArgs():
    " setup logging, parse command line arguments and options. -h shows auto-generated help page "
    parser = optparse.OptionParser("""usage: %prog [options] command - download gene model files and auto-detect the version.

    Commands for using gene models:
    fetch <geneType> - download pre-built geneId -> symbol table from UCSC
    fetch <assembly>.<geneType> - download pre-built gene models and symbol table from UCSC
    guess <inFile> <organism> - Guess best gene type. Reads the first tab-sep field from inFile and prints genetypes sorted by % of matching unique IDs to inFile.
    check <inFile> <geneType> - Check how well genes match given geneType

    Commands for building new gene model files:
    build <assembly>.<geneType> - Download a gene model file from UCSC, pick one transcript per gene and save to ~/cellbrowserData/genes/<db>.<geneType>.bed.gz and <geneType>.symbols.tsv.gz
    allSyms [human|mouse] - Build one big table with geneId <-> symbol, valid for all Gencode versions, always use most recent symbol
    add fname geneType - Add a two-column .tsv file to your local directory. First column is gene ID, second column is symbol.
                         e.g. 'cbGenes add myGenes.tsv sea-anemone'
    index - Build the -unique index files and also run 'allSyms' for both human and mouse
    push - Only at UCSC: copy all gene files to the export directory on hgwdev

    Run "fetch" or "build" without arguments to list the available files at UCSC.

    ls - list all available (built or downloaded)  gene models on this machine

    Examples (common):
    %prog fetch                   # show the files that are available for the 'build' command
    %prog fetch gencode-34        # geneId -> symbol mapping for human gencode relase 34
    %prog fetch hg38.gencode-34   # gene -> chrom mapping for human gencode relase 34
    %prog ls
    %prog guess genes.txt mouse   # guess the best gencode version for this file
    %prog check features.tsv.gz gencode-40 # check if the genes match gencode-40 and which ones don't

    Examples (rare - if you build your own gene models):
    %prog build                   # show the files that are available
    %prog build mm10 gencode-M25
    %prog index # used at UCSC to prepare the files for 'guess'
    %prog allSyms human # build big geneId -> symbol table from all 
    """)

    parser.add_option("-d", "--debug", dest="debug", action="store_true", help="show debug messages")
    (options, args) = parser.parse_args()

    if args==[] or (args[0]=="guess" and len(args)==1):
        parser.print_help()
        exit(1)

    setDebug(options.debug)
    return args, options

# ----------- main --------------
def parseSignatures(org, geneIdType):
    " return dict with gene release -> list of unique signature genes "
    ret = {}
    logging.info("Parsing gencode release signature genes")
    fname = getStaticFile("genes/%s.%s.unique.tsv.gz" % (org, geneIdType))
    logging.info("Parsing %s" % fname)
    genes = set()
    verToGenes = {}
    for line in openFile(fname):
        if line.startswith("#"):
            continue
        version, geneIds = line.rstrip("\n").split('\t')
        geneIds = set(geneIds.split("|"))
        verToGenes[version] = geneIds

    return verToGenes
        
def guessGeneIdType(genes):
    " return tuple organism / identifier type "
    logging.debug("Trying to guess organism and identifier type (syms or ids)")
    gene1 = list(genes)[0]
    if gene1.startswith("ENSG"):
        return "human", "ids"
    if gene1.startswith("ENSMUS"):
        return "mouse", "ids"

    upCount = 0
    for g in genes:
        if g.isupper():
            upCount += 1

    logging.debug("%d of %d genes are uppercase" % (upCount, len(genes)))
    if upCount/float(len(genes)) > 0.8:
        return "human", "syms"
    else:
        return "mouse", "syms"

def parseGenes(fname):
    " return gene IDs in column 1 of file "
    fileGenes = set()
    headDone = False
    logging.info("Parsing first column from %s" % fname)
    sep = sepForFile(fname)
    for line in openFile(fname):
        if not headDone:
            headDone = True
            continue
        geneId = splitOnce(line[:50], sep)[0]
        geneId = geneId.strip("\n").strip("\r").strip()
        #fileGenes.add(geneId.split('.')[0].split("|")[0])
        fileGenes.add(geneId.split("|")[0])
    logging.info("Read %d genes" % len(fileGenes))
    return fileGenes

def guessGencodeVersion(fileGenes, signGenes, stripVersion):
    logging.info("Number of genes that are only in a gene model release:")
    infos = []
    if stripVersion:
        fileGenes = set([x.split(".")[0] for x in fileGenes])

    for version, uniqGenes in signGenes.items():
        if stripVersion:
            uniqGenes = set([x.split(".")[0] for x in uniqGenes])

        intersection = list(fileGenes.intersection(uniqGenes))
        share = 100.0 * (float(len(intersection)) / len(uniqGenes))
        intLen = len(intersection)
        geneCount = len(uniqGenes)
        infoStr = "release "+version+": %0.2f%%, %d out of %d" % (share, len(intersection), len(uniqGenes))
        if len(intersection)!=0:
            expStr = ", ".join(intersection[:5])
            infoStr += (" e.g. "+ expStr)
        infos.append((share, version, intLen, geneCount, infoStr))

    infos.sort(reverse=True)
    bestRelease = infos[0][1]

    for info in infos:
        share, version, intLen, geneCount, infoStr = info
        print(infoStr)

    return bestRelease

def countDots(inGenes):
    " count how many gene names have a dot in them "
    c = 0
    for g in inGenes:
        if "." in g:
            c+=1
    return c

def guessNeedsStripping(inGenes):
    " return True if comparisons should be done without version information "
    dotCount = countDots(inGenes)
    if dotCount==len(inGenes):
        logging.info("All gene names have a dot in them. Assuming that input genes have a version")
        stripVersion  = False
    elif dotCount==0:
        logging.info("No gene ID has a dot in it. Stripping all version strings for the comparisons.")
        stripVersion = True
    else:
        logging.info("%d input genes have a dot in them, out of %d genes in total. Assuming that genes are symbols and not stripping the part after the dot.." % (dotCount, len(inGenes)))
        stripVersion  = True
    return stripVersion

def checkGenesAgainstRelease(inGenes, geneType, bestRelease, stripVersion):
    " output how well a release matches the input genes "
    allIds = readGeneSymbols(bestRelease)
    if stripVersion:
        inGenes = set([x.split(".")[0] for x in inGenes])
        allIds = set([x.split(".")[0] for x in allIds])

    if geneType=="syms":
        allIds = allIds
    notFoundIds = inGenes - set(allIds)
    print("%d of the genes in the input are not part of %s" % (len(notFoundIds), bestRelease))
    print("Examples: %s" % " ".join(list(notFoundIds)[:50]))

def guessGencode(fname, org):
    inGenes = parseGenes(fname)
    stripVersion = guessNeedsStripping(inGenes)

    inGenes = set(inGenes)
    guessOrg, geneType = guessGeneIdType(inGenes)
    if org is None:
        org = guessOrg
    else:
        logging.info("Organism was provided on command line: %s (no need to guess organism)" % org)
    logging.info("Assuming organism %s, IDs are %s" % (org, geneType))
    signGenes = parseSignatures(org, geneType)
    bestRelease = guessGencodeVersion(inGenes, signGenes, stripVersion)
    print("Best %s Gencode release\t%s" % (org, bestRelease))

    checkGenesAgainstRelease(inGenes, geneType, bestRelease, stripVersion)

def buildSymbolTable(geneType):
    if geneType.startswith("gencode"):
        release = geneType.split("-")[1]
        rows = iterGencodePairs(release)
    else:
        errAbort("unrecognized gene type '%s'" % geneType)

    outFname = getStaticPath(getGeneSymPath(geneType))
    writeRows(rows, outFname)

def iterGencodePairs(release, doTransGene=False):
    " generator, yields geneId,symbol or transId,geneId pairs for a given gencode release"
    # e.g. trackName = "wgEncodeGencodeBasicV34"
    #attrFname = trackName.replace("Basic", "Attrs").replace("Comp", "Attrs")
    #assert(release[1:].isdigit())
    db = "hg38"
    if release[0]=="M":
        db = "mm10"
        if int(release.strip("M"))>=26:
            db='mm39'
    if release in ["7", "14", "17", "19"] or "lift" in release:
        db = "hg19"
    url = "https://hgdownload.cse.ucsc.edu/goldenPath/%s/database/wgEncodeGencodeAttrsV%s.txt.gz" %  (db, release)
    logging.info("Downloading %s" % url)
    doneIds = set()

    lines = downloadUrlLines(url)
    for line in lines:
        row = line.rstrip("\n").split("\t")

        if doTransGene:
            # key = transcript ID, val is geneId
            key = row[4]
            val = row[0]
            val = val
        else:
            # key = geneId, val is symbol
            key = row[0]
            key = key
            val = row[1]

        if key not in doneIds:
            yield key, val
            doneIds.add(key)

def iterGencodeBed(db, release):
    " generator, yields a BED12+1 with a 'canonical' transcript for every gencode comprehensive gene "
    transToGene = dict(iterGencodePairs(release, doTransGene=True))

    url = "http://hgdownload.cse.ucsc.edu/goldenPath/%s/database/wgEncodeGencodeCompV%s.txt.gz" % (db, release)
    logging.info("Downloading %s" % url)
    geneToTransList = defaultdict(list)
    for line in downloadUrlLines(url):
        row = tuple(line.split('\t'))
        transId = row[1]
        geneId = transToGene[transId]
        score = int(''.join(c for c in geneId if c.isdigit())) # extract only the xxx part of the ENSGxxx ID
        geneToTransList[geneId].append( (score, row) )

    logging.info("Picking one transcript per gene")
    for geneId, transList in iterItems(geneToTransList):
        transList.sort() # prefer older transcripts
        canonTransRow = transList[0][1]
        binIdx, name, chrom, strand, txStart, txEnd, cdsStart, cdsEnd, exonCount, exonStarts, exonEnds, score, name2, cdsStartStat, cdsEndStat, exonFrames = canonTransRow
        blockStarts = []
        blockLens = []
        for exonStart, exonEnd in zip(exonStarts.split(","), exonEnds.split(",")):
            if exonStart=="":
                continue
            blockSize = int(exonEnd)-int(exonStart)
            blockStarts.append(exonStart)
            blockLens.append(str(blockSize))
        newRow = [chrom, txStart, txEnd, geneId, score, strand, cdsStart, cdsEnd, exonCount, ",".join(blockLens), ",".join(blockStarts), name2]
        yield newRow

def writeRows(rows, outFname):
    with openFile(outFname, "wt") as ofh:
        for row in rows:
            ofh.write("\t".join(row))
            ofh.write("\n")
    logging.info("Wrote %s" % outFname)

def buildLocusBed(db, geneType):
    " build a BED file with a 'canonical' transcript for every gene and a json file for it "
    if geneType.startswith("gencode"):
        release = geneType.split("-")[1]
        rows = iterGencodeBed(db, release)
    else:
        errAbort("Unknown gene model type: %s" % geneType)

    outFname = getStaticPath(getGeneBedPath(db, geneType))
    writeRows(rows, outFname)

    jsonFname = getStaticPath(getGeneJsonPath(db, geneType))
    bedToJson(db, geneType, jsonFname)

def listModelsLocal():
    " print all gene models on local machine "

    dataDir = join(findCbData(), "genes")
    print("Local cell browser genes data directory: %s" % dataDir)
    fnames = glob.glob(join(dataDir, "*.symbols.tsv.gz"))
    names = [basename(x).split(".")[0] for x in fnames]
    print("Installed gene/symbol mappings:")
    print("\n".join(names))
    print()

    fnames = glob.glob(join(dataDir, "*.bed.gz"))
    names = [basename(x).replace(".bed.gz","") for x in fnames]
    print("Installed gene/chrom-location mappings:")
    print("\n".join(names))

def addFileLocal(fname, name):
    " add a file to the local sym table dir"
    dataDir = join(findCbData(), "genes")
    newFname = name+".symbols.tsv.gz"
    newPath = join(dataDir, newFname)

    lines = open(fname).readlines()
    ofh = gzip.open(newPath, "wt")
    for l in lines:
        assert("\t" in l) # every line must contain at least one tab character
        l = l.strip() # we're getting DOS and Mac line endings sometimes...
        ofh.write(l)
        ofh.write("\n")
    ofh.close()
    logging.info("Wrote %s" % newPath)
    logging.info("You can now use the value '%s' in your cellbrowser.conf file as a value for geneIdType" % name)

def pushLocal():
    " copy all local files to export directory "
    srcDir = join(findCbData(), "genes/")
    targetDir = "/usr/local/apache/htdocs-cells/downloads/cellbrowserData/genes/"
    cmd = ["rsync", "-rvzp", srcDir, targetDir]
    subprocess.run(cmd, check=True)
    logging.info("Updated files in %s" % targetDir)

def iterBedRows(db, geneIdType):
    " yield BED rows of gene models of given type "
    fname = getStaticPath(getGeneBedPath(db, geneIdType))
    logging.info("Reading BED file %s" % fname)
    with openFile(fname) as ofh:
        for line in ofh:
            row = line.rstrip("\n\r").split("\t")
            yield row

def parseApacheDir(lines):
    fnames = []
    for l in lines:
        hrefCount = l.count("<a href=")
        if hrefCount==1:
            if "Parent Directory<" in l: 
                continue
            fname = l.split('<a href="')[1].split('"')[0]
            fnames.append(fname)
    return fnames

def listModelRemoteFetch():
    " print all gene models that can be downloaded "
    url = join(getDownloadsUrl(), "genes")
    lines = downloadUrlLines(url)
    fnames = parseApacheDir(lines)
    geneFnames = [f.replace(".bed.gz","") for f in fnames if f.endswith(".bed.gz")]
    symFnames = [f.replace(".symbols.tsv.gz", "") for f in fnames if f.endswith(".symbols.tsv.gz")]

    sep = "\n"

    print("Pre-built gene model mapping files available for 'fetch' at %s" % url)
    print(sep.join(geneFnames))
    #for g in geneFnames:
        #print(g.replace(".bed.gz",""))

    print()
    print("Pre-built geneId/symbol tables available for 'fetch' at %s" % url)
    print(sep.join(symFnames))
    #for g in symFnames:
        #print(g.replace(".symbols.tsv.gz", ""))

def listModelRemoteBuild():
    sep = "\n"
    urls = [("hg38", "https://hgdownload.cse.ucsc.edu/goldenPath/hg38/database/"),
            ("mm10", "https://hgdownload.cse.ucsc.edu/goldenPath/mm10/database/"),
            ("mm39", "https://hgdownload.cse.ucsc.edu/goldenPath/mm39/database/"),
            ("hg19", "https://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/")
            ]

    allNames = defaultdict(list)
    for db, url in urls:
        print()
        print("Files available for 'build' for assembly %s (%s)" % (db, url))
        lines = downloadUrlLines(url)
        fnames = parseApacheDir(lines)
        geneFnames = [x for x in fnames if x.startswith("wgEncodeGencodeAttrs") and x.endswith(".txt.gz")]
        relNames = [x.replace("wgEncodeGencodeAttrsV", "gencode-").replace(".txt.gz", "") for x in geneFnames]
        allNames[db].extend(relNames)
        print(sep.join(relNames))

    #for db, names in allNames.items():
        #for name in names:
            ##print("%s\t%s" % (db, name))
            #print(name)

def keepOnlyUnique(dictSet):
    """ give a dict with key -> set, return a dict with key -> set, but only with elements in the set that
    that don't appear in any other set
    """
    uniqVals = {}
    for key1, origVals in dictSet.items():
        vals = set(list(origVals))

        for key2 in dictSet.keys():
            if key1==key2:
                continue
            vals = vals - dictSet[key2]
        uniqVals[key1] = vals

    setList = list(dictSet.values())
    allCommon = set.intersection(*setList)
    return uniqVals, len(allCommon)

def writeUniqs(dictSet, outFname):
    " wrote to output file in format <key>tab<comma-sep-list of vals> "
    logging.info("Writing to %s" % outFname)
    with openFile(outFname, "wt") as ofh:
        for key, vals in dictSet.items():
            ofh.write("%s\t%s\n" % (key, "|".join(vals)))

def bigSymTable(org):
    """ build one big table that covers all gencode releases for an organism, org can be "mouse" or "human"
    """
    logging.info("Processing: %s" % org)
    infileMask = "gencode*.symbols.tsv.gz"
    dataDir = join(findCbData(), "genes")
    fnames = glob.glob(join(dataDir, infileMask))

    filtFnames = []
    for fname in fnames:
        baseName = basename(fname)
        # skip weird hg19 files and the big existing tables
        if ("lift" in baseName or "mouse" in baseName or "human" in baseName or "hg19" in baseName):
            continue
        version = baseName.split(".")[0].split("-")[1].lower()
        if (org=="human" and not "m" in version) or \
            (org=="mouse" and "m" in version):
            filtFnames.append((int(version.strip("m")), fname))

    filtFnames.sort()

    # read in order, such that new symbols overwrite old ones
    geneToSym = {}
    for idx, fname in filtFnames:
        logging.info("Reading "+fname)
        for line in openFile(fname):
            row = line.rstrip("\n").split("\t")
            geneId, sym = row[:2]
            geneId = geneId.split(".")[0]
            geneToSym[geneId] = sym

    outFname = getStaticPath(getGeneSymPath("gencode-"+org))

    writeRows(geneToSym.items(), outFname)

def uniqueIds(org):
    """ find unique identifiers in all symbols and geneIds of infileMask and write to
    outBase.{syms,ids}.unique.syms.tsv.gz
    """
    logging.info("Processing: %s" % org)
    infileMask = "gencode*.symbols.tsv.gz"
    dataDir = join(findCbData(), "genes")
    fnames = glob.glob(join(dataDir, infileMask))
    allSyms = {}
    allIds = {}
    for fname in fnames:
        baseName = basename(fname)
        if "lift" in baseName or "mouse" in baseName or "human" in baseName:
            continue
        if org=="human" and "M" in baseName:
            continue
        if org=="mouse" and not "M" in baseName:
            continue
        geneType = basename(fname).split(".")[0]
        logging.info("Reading %s" % fname)

        syms = set()
        ids = set()
        for line in openFile(fname):
            row = line.rstrip("\n").split("\t")
            geneId, sym = row[:2]
            syms.add(sym)
            ids.add(geneId)
        allSyms[geneType] = syms
        allIds[geneType] = ids

    # force refseq into this
    syms = []
    fname = getStaticFile("genes/entrez-%s.symbols.tsv.gz" % (org))
    for line in openFile(fname):
        if line.startswith("#"):
            continue
        geneId, sym = line.rstrip("\n").split("\t")
        syms.append(sym)
    allSyms["entrez"] = set(syms)

    logging.info("Finding unique values")
    uniqSyms, commonSyms = keepOnlyUnique(allSyms)
    uniqIds, commonIds = keepOnlyUnique(allIds)
    logging.info("%d symbols and %d geneIds are shared among all releases" % (commonSyms, commonIds))

    writeUniqs(uniqSyms, join(dataDir, org+".syms.unique.tsv.gz"))
    writeUniqs(uniqIds, join(dataDir, org+".ids.unique.tsv.gz"))

def bedToJson(db, geneIdType, jsonFname):
    " convert BED file to more compact json file: chrom -> list of (start, end, strand, gene) "
    geneToSym = readGeneSymbols(geneIdType)

    # index transcripts by gene
    bySym = defaultdict(dict)
    for row in iterBedRows(db, geneIdType):
        chrom, start, end, geneId, score, strand = row[:6]
        sym = geneToSym[geneId]
        start = int(start)
        end = int(end)
        transLen = end-start
        rawGeneId = geneId.split(".")[0] # for lookups, we hopefully will never need the version ID...
        fullGeneId = rawGeneId+"|"+sym
        bySym[fullGeneId].setdefault(chrom, []).append( (transLen, start, end, strand, geneId) )

    symLocs = defaultdict(list)
    for geneId, chromDict in bySym.items():
        for chrom, transList in chromDict.items():
            transList.sort(reverse=True) # take longest transcript per chrom
            _, start, end, strand, transId = transList[0]
            symLocs[chrom].append( (start, end, strand, geneId) )

    sortedLocs = {}
    for chrom, geneList in symLocs.items():
        geneList.sort()
        sortedLocs[chrom] = geneList

    ofh = open(jsonFname, "wt")
    outs = json.dumps(sortedLocs)
    #md5 = hashlib.md5(outs.encode("utf8")).hexdigest()[:10]
    ofh.write(outs)
    ofh.close()
    logging.info("Wrote %s" % jsonFname)
    logging.info("If this is a new .json file and you are on hgwdev, copy it now to /usr/local/apache/htdocs-cells/downloads/cellbrowserData/genes/ and note this directory for the dataset release push to the RR. The reason is that users may want to cbBuild using this gene transcript set and that is easier if we provide the .json file")

    #fileInfo[code] = {"label":label, "file" : jsonFname, "md5" :md5}

def buildGuessIndex():
    " read all gene model symbol files from the data dir, and output <organism>.unique.tsv.gz "
    dataDir = join(findCbData(), "genes")
    uniqueIds("human")
    uniqueIds("mouse")
    bigSymTable("human")
    bigSymTable("mouse")

def fetch(fileDesc):
    " download symbol or gene files to local dir "
    if "." in fileDesc:
        # user wants a gene model file
        ext = "bed.gz"
    else:
        ext = "symbols.tsv.gz"
    fname = getStaticFile("genes/%s.%s" % (fileDesc, ext), verbose=True)
    return

def cbGenesCli():
    args, options = cbGenes_parseArgs()

    command = args[0]
    if command=="guess":
        fname = args[1]
        org = None
        if len(args)==3:
            org = args[2]
        guessGencode(fname, org)

    elif command == "check":
        fname = args[1]
        release = args[2]
        inGenes = parseGenes(fname)
        guessOrg, geneType = guessGeneIdType(inGenes)
        stripVersion = guessNeedsStripping(inGenes)
        checkGenesAgainstRelease(inGenes, geneType, release, stripVersion)

    elif command=="fetch":
        if len(args)==1:
            listModelRemoteFetch()
        else:
            arg = args[1]
            fetch(arg)

    elif command=="syms": # undocumented
        geneType = args[1]
        buildSymbolTable(geneType)

    elif command=="build":
        if len(args)==1:
            listModelRemoteBuild()
        else:
            db, geneType = args[1:]
            buildSymbolTable(geneType)
            buildLocusBed(db, geneType)

    elif command=="ls":
        listModelsLocal()

    elif command=="index":
        buildGuessIndex()

    elif command=="allSyms":
        org = args[1]
        bigSymTable(org)

    elif command=="add":
        addFileLocal(args[1], args[2])

    elif command=="push":
        pushLocal()

    elif command=="json": # undocumented
        db, geneType, outFname = args[1:]
        bedToJson(db, geneType, outFname)
    else:
        errAbort("Unrecognized command: %s" % command)


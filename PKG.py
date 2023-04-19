import os, sys

def progressbar(it, prefix="", size=60, out=sys.stdout, char=u"█"): # Python3.3+
    count = len(it)
    def show(j):
        x = int(size*j/count)
        print("{}[{}{}] {}/{}".format(prefix, char*x, "."*(size-x), j, count),
                end='\r', file=out, flush=True)
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    print("\n", flush=True, file=out)

def MakeFile(filePaths, fileNames, fileToWrite = 'spriteSet.dmlp'):
    data = []
    for file in filePaths:
        with open(file, 'rb') as fh:
            data.append(fh.read())

    raw = b''
    for i in range(len(data)):
        raw += bytes(data[i]) + b'{}{}{}{}{}' + bytes(str(fileNames[i]), encoding='utf-8') + b'\n\n\n\n\n\n'
    with open(fileToWrite, 'wb') as fh:
        fh.write(raw)

def ReadFile(toRead = "spriteSet.dmlp", FinalPath = 'fromPKG/'):
    with open(toRead, 'rb') as fh:
        raw = fh.read()
    imgs = raw.split(b'\n\n\n\n\n\n')
    for i in progressbar(it=range(len(imgs)), prefix="READING: ", size=40, char='~'):
        img = imgs[i]
        if img != b'':
            imgName = str(img.split(b'{}{}{}{}{}')[1])
            finalName = ''
            for i in range(len(imgName)):
                char = imgName[i]
                if i != 0 and i != 1 and i != len(imgName)-1:
                    finalName = finalName + char
            imgCont = img.split(b'{}{}{}{}{}')[0]
            with open(f'{FinalPath}{finalName}', 'wb') as fh:
                fh.write(imgCont)

def FindAllFilesInDir(rootPath ='Assets'):
    filesToPack = []
    filePaths = []
    for path, subdirs, files in os.walk(rootPath):
        for file in files:
            filesToPack.append(file)
            filePaths.append((path + '/' + file))
    return [filePaths, filesToPack]

try:
    command = str(sys.argv[1]).upper()
except IndexError:
    command = 'HELP'

match command:
    case 'HELP':
        print("HOW TO FORMAT A COMMAND: \n"
              "1. USE COMMAND KEYWORD (COMP_DIR or DECOMP_PKG)\n"
              "2. ENTER PARAMETERS (PLACED AFTER THE : IN THE DIRECTIONS)\n"
              "\n EX: python PKG.py COMP_DIR ASSETS assets.dmlp\n"
              "COMMANDS:\n"
              "\n     - COMP_DIR: DirectoryPath, FinalOutputPath"
              "\n     - DECOMP_PKG: path/to/PKG, FinalDecompressionPath"
              "\nP.S. All arguments are optional but it probably won't do what you want\n")
    case 'COMP_DIR':
        if len(sys.argv) > 2:
            paths = FindAllFilesInDir(rootPath=sys.argv[2])
        else:
            paths = FindAllFilesInDir()
        fPaths = paths[0]
        fToPack = paths[1]
        match len(sys.argv):
            case 1:
                pass
            case 2:
                pass
            case 3:
                pass
            case 4:
                MakeFile(fPaths, fToPack, sys.argv[3])
        print("SUCCESSFUL COMPRESSION")
    case 'DECOMP_PKG':
        match len(sys.argv):
            case 3:
                ReadFile(sys.argv[2])
            case 4:
                ReadFile(sys.argv[2], sys.argv[3])
            case _:
                ReadFile()

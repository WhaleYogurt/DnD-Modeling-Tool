import os, sys
from functions import progressbar

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

def FindAllFiles(rootPath = 'Assets'):
    filesToPack = []
    filePaths = []
    for path, subdirs, files in os.walk(rootPath):
        for file in files:
            filesToPack.append(file)
            filePaths.append((path + '/' + file))
    return [filePaths, filesToPack]

command = sys.argv[1]

if command == 'MakePKG':
    fPaths = FindAllFiles()[0]
    fToPack = FindAllFiles()[1]
    MakeFile(fPaths, fToPack)
elif command == 'UnpackPKG':
    ReadFile()
else:
    raise Exception("PLEASE ENTER A VALID COMMAND\n LIKE 'MakePKG' or 'UnpackPKG'")

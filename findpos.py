import sys
import os
import glob
import ntpath
from pathlib import Path
from shutil import copy

def main():
    if not len(sys.argv) == 4:
        print("Usage: python findpos.py <file.csv> <folder> <targetFolder>")
        sys.exit(-1)
    
    csvFile = sys.argv[1]
    folder = sys.argv[2]
    targetFolder = sys.argv[3]

    prefixFolder = getFileName(csvFile)
    prefixFolder = prefixFolder[0:(len(prefixFolder) - 4)]
    
    # Verify if file.csv exists
    if not os.path.isfile(csvFile):
        print("The file " + csvFile + " does not exist")
        sys.exit(-1)
    
    # Verify if folder exists
    if not os.path.exists(folder):
        print("The folder " + folder + " does not exist")
        sys.exit(-1)

    # Verify if the target folder exists
    if not os.path.exists(targetFolder):
        os.mkdir(targetFolder)
    
    readFile(csvFile, folder, targetFolder, prefixFolder)

    sys.exit(0)

def readFile(csvFile, folder, targetFolder, prefixFolder):
    f = open(csvFile, "r")
    for x in f:
        parts = x.split(",")
        poKey = parts[0]
        poName = parts[1].replace("\n", "")
        print("")
        print("-" * 10 + poKey + "-" * 10)

        # find BSCS POs
        resultBSCS = searchFiles(poName + ".xml", folder)
        if len(resultBSCS) == 0:
            print("No BSCS POs found")
        else:
            processItems(resultBSCS, targetFolder, prefixFolder, poKey, 'bscs')

        # find ECM POs
        resultECM = searchFiles(poName + ".zip", folder)
        if len(resultECM) == 0:
            print("No ECM POs found")
        else:
            processItems(resultECM, targetFolder, prefixFolder, poKey, 'ecm')
        
        # find CS POs
        resultCS = searchFiles("*" + poKey + "*.xml", folder)
        if len(resultCS) == 0:
            print("No CS POs found")
        else:
            processItems(resultCS, targetFolder, prefixFolder, poKey, 'cs')
    f.close()

def processItems(result, targetFolder, prefixFolder, poKey, poType):
    if poType == "cs":
        items = result
    else:
        items = result[-1:]

    for item in items:
        fileName = getFileName(item)
        onlyFolder = os.path.join(targetFolder, prefixFolder, poKey, poType)
        if not os.path.exists(onlyFolder):
            os.makedirs(onlyFolder)

        finalTarget = os.path.join(onlyFolder, fileName)
        print("copying " + fileName + " to " + onlyFolder)
        copy(item, finalTarget)

def searchFiles(criteria, folder):
    result = []
    for path in Path(folder).rglob(criteria):
        result.append(path)
    
    result.sort()

    return result

def getFileName(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)  


if __name__ == "__main__" :
    main()
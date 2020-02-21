import sys
import os
import glob
import ntpath

def main():
    if not len(sys.argv) == 3:
        print("Usage: python findpos.py <file.csv> <folder>")
        sys.exit(-1)
    
    csvFile = sys.argv[1]
    folder = sys.argv[2]
    
    # Verify if file.csv exists
    if not os.path.isfile(csvFile):
        print("The file " + csvFile + " does not exist")
        sys.exit(-1)
    
    # Verify if folder exists
    if not os.path.exists(folder):
        print("The folder " + folder + " does not exist")
        sys.exit(-1)
    
    print("Validaciones correctas de archivos y carpetas")
    
    sys.exit(0)

if __name__ == "__main__" :
    main()
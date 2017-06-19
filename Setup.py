##################################################################################################################
# Setup.py
##################################################################################################################
# Author: Christina Kim
# Date: 19 June 2017
# Description: Remove test data files generated from the previous run
##################################################################################################################

import os
import shutil


#Used to resolve the issue that folders are set to 'Read Only' access after they are copied., which causes an 'Access error' when trying to remove those folders
def handleRemoveReadonly(func, path, exc):
    excvalue = exc[1]
    if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) 
        func(path)
    else:
        raise

# Remove test data files generated from the previous run
def removeTestFiles(testDataFolder):
    #os.remove(testDataFolder + folderPrefix + i_str + "\\" + currFolder + ".json")
    #errorFileList = os.listdir(errorLogPath)
    testFileList = os.listdir(testDataFolder)
    sampleDataList = ['IFC_UAT100084', 'IFC_UAT100085', 'IFC_UAT100086', 'IFC_UAT100087', 'UPDATE_20170411_10_04_55_214.json']

    #Iterate all the files/ directories and remove everything except what are used as the base test files
    for each in testFileList:
        if (each not in sampleDataList):
            if(os.path.isdir(testDataFolder + "\\" + each)):
                shutil.rmtree(testDataFolder + "\\" + each, ignore_errors=False, onerror=handleRemoveReadonly)
            else:
                os.remove(testDataFolder + "\\" + each)
    

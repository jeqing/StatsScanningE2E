##################################################################################################################
# Gen_test_files.py
##################################################################################################################
# Author: Ben Schluter
# Date: 15 May 2017
# Description: Duplicate test input folders a specified number of times, modifying the folder JSON files
# as well as appending a form type record to the detail JSON file, both with new GUIDs for testing
# The original script has been decomposed by Christina Kim
##################################################################################################################

import os
import shutil
import uuid
import sys
from glob import glob
import datetime
#import ReplaceDocIds

# Check if a directory or a file exists
def checkFileExist(fileType, dataFolder, jSonFile = None ):
    if fileType == 'dir': 
        if not (os.path.isdir(dataFolder)): # Check test Data folder exists
            print ("Error: Test data Folder: " + dataFolder + " not found!")
            sys.exit(1)   
    
    else:                                        # Meaning that fileType == 'file'
        if not (os.path.isfile(dataFolder + jSonFile)):         # Check detail JSON file exists
            print ("Error: Detail JSON File: " + jSonFile + " not found!")
            sys.exit(1)        


def getImages(dataFolder, folderPrefix): # Retrieve all test image folders and exit if no image folder is found
    os.chdir(dataFolder)
    folderList = glob(folderPrefix + "*\\")  
    
    # Check there are test image folders present
    if len(folderList) == 0:
        print ("Error: No test folders of prefix: " + folderPrefix + " found!")
        sys.exit(1)    
    return folderList


# Get last folder suffix used for test folders
def getLastFolderSuffix(folderList, folderPrefix):
    iter = 0
    for folder in folderList:
        intSuffix = int(folder[len(folder)-7:len(folder)-1])
        if (intSuffix > iter):
            iter = intSuffix 
    return iter


def replaceGUID(docIdGuidList, currFolder, itemList, sampleDataFolder, testDataFolder, folderPrefix, i_str):
   
    # For each image
    detailName = currFolder[8:15]
    inputJsonFile = sampleDataFolder + detailName + ".json"

    # Read in Detail Json file to memory, remove last closing brace
    detailJson = open(inputJsonFile,"r")
    detailLine = detailJson.read()
    detailJson.close()             
    
    for item in itemList:
        # Generate new GUID
        newGuidId = uuid.uuid4()

        newName = str(newGuidId) + item[36:]
        # Rename the image file
        os.rename(testDataFolder + folderPrefix + i_str + "\\" + item,testDataFolder + folderPrefix + i_str + "\\" + newName)

        oldId = item[0:36]

        # Replace GUID in the detail JSON file
        startPos = detailLine.find(oldId)
        
        newLine = detailLine.replace(oldId, str(newGuidId))


        submittedPos = newLine.find("\"submitted_date_time\":",startPos)
        if (submittedPos == -1):
            print ("Error: Submitted date time field not found in detail JSON file") 
            sys.exit(1)        
        
        validationPos = detailLine.find("\"validation_status\":",startPos)
        if (validationPos == -1):
            print ("Error: Validation Status field not found in detail JSON file") 
            sys.exit(1)                
        
        jsonDateStamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        print (jsonDateStamp)
        
        newLine = detailLine[0:submittedPos+23] + jsonDateStamp + detailLine[validationPos-2:]
        detailLine = newLine
        
        docIdPos = detailLine.find("document_id",startPos)
        oldDocId = detailLine[docIdPos+14: docIdPos+23]
        
        #detailLine = detailLine.replace(oldDocId, "12345")
        #detailLine = detailLine.replace("613948850", "12345")
        
        
        oldDocIDs = ["642124311", "613948850"]
        newDocIDs = ["000", "111"]
        i = 0
        while (i < len(oldDocIDs)):
            detailLine = detailLine.replace(oldDocIDs[i], newDocIDs[i])        
            docIdGuidList.append((newDocIDs[i], str(newGuidId)))
            i += 1
  
        
              
    
    outputJsonFile = 'UPDATE_'+ detailName + "_" + datetime.datetime.now().strftime('%Y%m%d_%H_%M_%S_214') + '.json'
    finalJson = open(testDataFolder + outputJsonFile,"w")
    finalJson.write(detailLine)
    finalJson.close()       
        
    
    return docIdGuidList        

      
    
    
def duplicateProcess(numberOfDuplicates, folderList, iter, sampleDataFolder, testDataFolder, folderPrefix):
   
    docIdGuidList = []
    # For number of test duplicates
    for i in range(numberOfDuplicates):
        # For each test image folder
        for j in range(len(folderList)):
            # Increment the folder suffix
            iter = iter + 1
            i_str = str(iter).strip()
            
            # Copy the image folder to the new folder
            shutil.copytree(sampleDataFolder + folderList[j], testDataFolder + folderPrefix + i_str)

            imageFolderList = os.listdir(testDataFolder + folderPrefix + i_str)
            itemList = []
                           
            # Find all tif image files in the folder
            for file in imageFolderList:
                if file.find(".tif") > 0:
                    itemList.append(file)
                    
            currFolder = folderList[j]
            
            docIdGuidList = replaceGUID(docIdGuidList, currFolder,itemList, sampleDataFolder, testDataFolder, folderPrefix, i_str)
    
    return docIdGuidList
    
    

def generateTestFiles(sampleDataFolder, testDataFolder, folderPrefix, numberOfDuplicates):
# Modify below parameters for testing
# Escape \ characters in paths with a leading \
    #testDataFolder = "C:\\Users\\azl-ckim\\Desktop\\CK\\E2E_Scanning\\Scanning Data Files\\"
    #detailJsonFile = "UPDATE_20170411_10_04_55_214.json"
    #folderPrefix = "IFC_UAT"

    #numberOfDuplicates = 1
    

    checkFileExist('dir', sampleDataFolder, )
    #checkFileExist('file', sampleDataFolder, detailJsonFile)
    
    folderList = getImages(sampleDataFolder, folderPrefix)

    iter = getLastFolderSuffix(folderList, folderPrefix)
    
    docIdGuidList = duplicateProcess(numberOfDuplicates, folderList, iter, sampleDataFolder, testDataFolder, folderPrefix)
    print(docIdGuidList)
    
    return docIdGuidList

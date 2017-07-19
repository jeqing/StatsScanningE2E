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
import time
import ReplaceDocIds
from random import randint


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


def replaceGUID(docIdGuidList, currFolder, imageFileList, sampleDataFolder, testDataFolder, folderPrefix, i_str, newDocIDs, origLine, newBatchID):
   
    # For each image
    detailName = currFolder[8:15]
    inputJsonFile = sampleDataFolder + detailName + ".json"

    # Read in Detail Json file to memory, remove last closing brace
    detailJson = open(inputJsonFile,"r")
    detailLine = detailJson.read()
    detailJson.close()             
    
    for item in imageFileList:
        # Generate new GUID
        newGuidId = uuid.uuid4()
        newDocID = None

        newName = str(newGuidId) + item[36:]
        if (item.find('642124311') > -1):
            newName = str(newGuidId) + "_" + newDocIDs[0] + item[46:]
            origLine = origLine.replace('642124311', newDocIDs[0])
            newDocID = newDocIDs[0]

        else:
            if (item.find('613948850') > -1):
                newName = str(newGuidId) + "_" + newDocIDs[1] + item[46:]
                origLine = origLine.replace('613948850', newDocIDs[1])
                newDocID = newDocIDs[1]
    
        # Rename the image file
        os.rename(testDataFolder + folderPrefix + i_str + "\\" + item,testDataFolder + folderPrefix + i_str + "\\" + newName)

        oldId = item[0:36]
        
    
        # Replace BatchID in the foldr Json file
        oldBatchID = origLine[11:17]
        print("oldBatchID: " + oldBatchID)
        print("newBatchID: " + str(newBatchID))
        origLine = origLine.replace(oldBatchID, str(newBatchID))
        
        # Replace GUID in the folder JSON file
        newLine = origLine.replace(oldId, str(newGuidId))
        origLine = newLine        

        

        # Replace GUID in the detail JSON file
        startPos = detailLine.find(oldId)
        
        newLine = detailLine.replace(oldId, str(newGuidId))
        detailLine = newLine

        submittedPos = newLine.find("\"submitted_date_time\":",startPos)
        if (submittedPos == -1):
            print ("Error: Submitted date time field not found in detail JSON file") 
            sys.exit(1)        
        
        validationPos = detailLine.find("\"validation_status\":",startPos)
        if (validationPos == -1):
            print ("Error: Validation Status field not found in detail JSON file") 
            sys.exit(1)                
        
        #jsonDateStamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        jsonDateStamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M') + ':' + str(randint(10, 59))
        
        newLine = detailLine[0:submittedPos+23] + jsonDateStamp + detailLine[validationPos-2:]
        detailLine = newLine
        # CK to change doc ids
        docIdPos = detailLine.find("document_id",startPos)
        oldDocId = detailLine[docIdPos+14: docIdPos+23]
              
        oldDocIDs = ["642124311", "613948850"]
  
  
        #i = 0
        #print(docIdGuidList)    
        #while (i < len(oldDocIDs)):
            #detailLine = detailLine.replace(oldDocIDs[i], newDocIDs[i])   
            #print("new item to docIdGuidList")
            #print(newDocIDs[i])
            #print(str(newGuidId))
            #docIdGuidList.append((newDocIDs[i], str(newGuidId)))
            #i += 1
        
        docIdGuidList.append((newDocID, str(newGuidId)))
    
    outputJsonFile = 'UPDATE_'+ detailName + "_" + datetime.datetime.now().strftime('%Y%m%d_%H_%M_%S') + '.json'
    finalJson = open(testDataFolder + outputJsonFile,"w")
    
    finalJson.write(detailLine)
    finalJson.close()       
 
    
    return origLine, docIdGuidList        

      
    
    
def duplicateProcess(numberOfDuplicates, folderList, iter, sampleDataFolder, testDataFolder, folderPrefix):
    newDocIDs = ReplaceDocIds.replaceDocIDs()
    
    docIdGuidList = []
    # For number of test duplicates
    for i in range(numberOfDuplicates):
        # For each test image folder
        for j in range(len(folderList)):
            # Increment the folder suffix
            iter = iter + 1
            i_str = str(iter).strip()
            
            # Copy the image folder to the new folder
            oldBatchID = folderList[j][len(folderList[j])-7: len(folderList[j]) -1]
            print("old file name: " + sampleDataFolder + folderList[j])
            print("new file name: " + testDataFolder + folderPrefix + i_str)
            shutil.copytree(sampleDataFolder + folderList[j], testDataFolder + folderPrefix + i_str)
            
            # Get current test folder removing the trailing folder separator '\'
            currFolderTmp = folderList[j]
            currFolder = currFolderTmp[:len(currFolderTmp)-1]            
            
            # Read in the folder JSON file
            json = open(testDataFolder + folderPrefix + i_str +"\\" + folderPrefix + oldBatchID + ".json","r")
            origLine = json.read()
            json.close()
        
            # Remove the folder JSON file
            os.remove(testDataFolder + folderPrefix + i_str +"\\" + folderPrefix + oldBatchID + ".json")
            imageFolderList = os.listdir(testDataFolder + folderPrefix + i_str)
            imageFileList = []
                           
            # Find all tif image files in the folder
            for file in imageFolderList:
                if file.find(".tif") > 0:
                    imageFileList.append(file)
                    
            currFolder = folderList[j]
            
            origLine, docIdGuidList = replaceGUID(docIdGuidList, currFolder, imageFileList, sampleDataFolder, testDataFolder, folderPrefix, i_str, newDocIDs, origLine, i_str)
            
            print("newjson: " + testDataFolder + folderPrefix + i_str + "\\" + folderPrefix + i_str + ".json")
            newJson = open(testDataFolder + folderPrefix + i_str + "\\" + folderPrefix + i_str + ".json","w")
            newJson.write(origLine)
            newJson.close()
            
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
    
    return docIdGuidList

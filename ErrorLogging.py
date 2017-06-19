##################################################################################################################
# ErrorLoggin.py
##################################################################################################################
# Author: Christina Kim
# Date: 19 June 2017
# Description: Generate error log files in the csv format.
##################################################################################################################

from time import gmtime, strftime

#Generated csv files with the given error lists.
def generateErrorLog(notFoundDataList, dataWithError, tableName, errorLogLocation, fieldsToSelectList):
    currentDateTime = strftime("%Y%m%d_%H_%M_%S", gmtime())

    #Log file for the data which has not been correctly loaded in the DB
    if (dataWithError != None and dataWithError != [] ):
        errorLog = open(errorLogLocation + tableName + "_" + currentDateTime + ".csv", "w")
        errorLog.write(','.join(fieldsToSelectList) + '\n')  # create headers                 
        for each in dataWithError:    
            count = len(each)
            index = 0
            resultList = []
            while (index < count):
                resultList.append(str(each[index]))
                index += 1
            errorLog.write(','.join(resultList) + '\n')
        errorLog.close()

    #Log file for the data which is not found in the DB at all.
    if(notFoundDataList != None and notFoundDataList != []):
        notFoundDataLog = open(errorLogLocation + tableName + "_NotFound" + currentDateTime + ".csv", "w")
        notFoundDataLog.write(','.join(["DocID", "Guid"]) + '\n')                
        for each in notFoundDataList:
            count = len(each)
            index = 0
            resultList = []
            while (index < count):
                resultList.append(str(each[index]))
                index += 1
            notFoundDataLog.write(','.join(resultList) + '\n')     
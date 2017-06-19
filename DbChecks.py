##################################################################################################################
# DbChecks.py
##################################################################################################################
# Author: Christina Kim
# Date: 19 June 2017
# Description: Connect to the SQL Server and check if Response Store DB and Markin DB have been updated correctly.
# Generated error log files if data has not been loaded properly.
##################################################################################################################

import pypyodbc  # to connect to DB
from time import gmtime, strftime
import ErrorLogging

#Connect to the SQL Server DB
def connectToDB(server, dataBase):
        con = pypyodbc.connect("DRIVER={SQL Server}; SERVER=" + server + ";DATABASE=" + dataBase + ";")
        cursor = con.cursor()
        return cursor
                        

# check data in DB and populate a csv file with data with errors
def executeQuery(server, dataBase, tableName, docIdGuidList, fieldToIdentify, fieldToCheckInDB, valuetoCheckAgainst, errorLogLocation, fieldsToSelectList):
        cursor = connectToDB(server, dataBase)
        fieldsToSelectString = ','.join(fieldsToSelectList)
        notFoundDataList = []  #Log file for the data which is not found in the DB at all.
        fetchedResultList = [] #Log file for the data which has not been correctly loaded in the DB
        print(docIdGuidList)
        indexToCheckInDocIdGuidList = 0  # this index is for DocID and used for Markin DB
        tableNameToList = tableName.split(".")
        dataWithError = None
        
        if (dataBase == 'StatsNZ_Epl_ResponseStore'): 
                indexToCheckInDocIdGuidList = 1   # Guid used for Response Store
                        
        if (tableNameToList[2] == "response_data_PublicReport_v"):
                print("response_data_PublicReport_v")
                for docIdGuidTuple in docIdGuidList:  
                        queryToFindData = "select " + fieldsToSelectString + " from " + tableName +" where " + fieldToIdentify + "=" + "'" + docIdGuidTuple[indexToCheckInDocIdGuidList] + "'"  
                        cursor.execute(queryToFindData)
                        if (cursor.rowcount == 0):  # No data found with given docId/ Guid
                                notFoundDataList.append(docIdGuidTuple)
        else:                
                if (tableNameToList[2] == "response_image_PublicReport_v"):
                        print("response_image_PublicReport_v")
                        for docIdGuidTuple in docIdGuidList:  
                                queryToFindData = "select " + fieldsToSelectString + " from " + tableName +" where " + fieldToIdentify + "=" + "'" + docIdGuidTuple[indexToCheckInDocIdGuidList] + "'"  
                                cursor.execute(queryToFindData)
                                query = None                                
                                if (cursor.rowcount == 0):  # No data found with given docId/ Guid
                                        notFoundDataList.append(docIdGuidTuple)
                                else: 
                                        query = queryToFindData + " and " + fieldToCheckInDB + " not like " + "'" + docIdGuidTuple[indexToCheckInDocIdGuidList] + "%'"  
                                if (query != None):
                                        queryResult = cursor.execute(query)                                
                                        dataWithError = queryResult.fetchall()
                                        print(dataWithError)
                                        fetchedResultList += dataWithError                                
                else: # tableNameToList[2]  == "CensusMarkinStatus"
                        print("CensusMarkinStatus")
                        for docIdGuidTuple in docIdGuidList:  
                                queryToFindData = "select " + fieldsToSelectString + " from " + tableName +" where " + fieldToIdentify + "=" + "'" + docIdGuidTuple[indexToCheckInDocIdGuidList] + "'"  
                                cursor.execute(queryToFindData)
                                query = None                                
                                if (cursor.rowcount == 0):  # No data found with given docId/ Guid
                                        notFoundDataList.append(docIdGuidTuple)     
                                
                                else: 
                                        query = queryToFindData + " and " + fieldToCheckInDB + "<>" + "'" + valuetoCheckAgainst +"'"
                                 
                                if (query != None):                
                                        queryResult = cursor.execute(query)                                
                                        dataWithError = queryResult.fetchall()
                                        print(dataWithError)
                                        fetchedResultList += dataWithError                                    
                
        notFoundDataSet = set(notFoundDataList)  # removing duplicate data
        cursor.close()
        
        #Generated error log files if there is any data which has not been loaded in the DB as expected
        if (notFoundDataSet != None or fetchedResultList != []):
                ErrorLogging.generateErrorLog(notFoundDataSet, fetchedResultList, tableName, errorLogLocation, fieldsToSelectList)

                         


        
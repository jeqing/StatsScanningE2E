###################################################################################################################################
# This scripts uses a Python package called "simple salesforce" to connect to salesforce and use the Salesforce query language 
# i.e. very similar to SQL and then traverses the response data strcture to print the Mark in status for an access code in salesforce 
# create by Ben,Christina and Sunjeet 14th June,2017
####################################################################################################################################


#Simple salesforce package that is being used for this Test script 
from simple_salesforce import Salesforce
import ErrorLogging


# connect to salesforce sandbox ( regression ) envrionment , using desired user name and password AND secuirty-token that can be retrieved from that SF instance --> 
# (under you user name) "my settings" hyperlink --> "personal" --> "reset my security token"


def connectToSalesForceDB(user, pw, token):
    sf = Salesforce(username = user, password = pw, security_token = token, sandbox = True)
    
    return sf

# run a SOQL query to select the mark in value from a response salesforce object , for a particular access code
# the documentation for exposed APIs can be found in Salesforce from set up --> Build --> create --> Objects 
def checkMarkInFromDB(salesForceConnection, partialQuery, docIdGuidList):
    notFoundDataList = []
    dataWithErrorList = []
    isMarkedIn = False
    for docIdGuidGuple in docIdGuidList:
        query = partialQuery + "'" + docIdGuidGuple[0] + "'"
        result = salesForceConnection.query_all(query)
        if (result == None):
           
            notFoundDataList.append(docIdGuidGuple)
        else: 
            record = (result['records'])
            if (record != []):
                an_dict = record[0] 
                isMarkedIn = an_dict['Mark_In__c']
            if (isMarkedIn != True):
                errorDataToBeLogged = (docIdGuidGuple[0], docIdGuidGuple[1], "Not MarkedIn")
                dataWithErrorList.append(errorDataToBeLogged)
    return notFoundDataList, dataWithErrorList

#This is the main function in this module and calls the other functions.
def checkDataInSalesForce(user, pw, token, query, docIdGuidList, errorLogLocation, headerList):
    sf = connectToSalesForceDB(user, pw, token)
    
    notFoundDataList, dataWithErrorList = checkMarkInFromDB(sf, query, docIdGuidList)
    if (notFoundDataList != [] or dataWithErrorList != []):
        ErrorLogging.generateErrorLog(notFoundDataList, dataWithErrorList, "SalesForce", errorLogLocation, headerList)







import os
import sys
import time
import random
import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from simple_salesforce import Salesforce
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import pypyodbc


class Logger:
    def __init__(self,logPrefix,logFolder):
    
        self.folder = logFolder
        self.filename = logPrefix + "_" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".txt"
        self.fileHandle = open(self.folder + self.filename,'w')
        self.errors = []
        self.numErrors = 0
        self.message = ""
        
    def writeToLog(self, text):
        currTime = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        self.fileHandle.write(currTime + " " + text + "\r\n")

        textUpper = text.upper()
        if (textUpper[0:5] == "ERROR"):
            self.errors.append(text)
            self.numErrors += 1

    def closeLog(self):
        if (self.numErrors == 0):
            self.message = "SUCCESS: No errors in log"
        else:
            self.message = "ERROR: " + str(self.numErrors).strip() + " errors found in log"
        self.fileHandle.close()
        self.emailLog()
        
    def emailLog(self):

        senderPw = "Stats12345"
        sender = "stats.integration.testing@gmail.com"
        recipient = "ben.schluter@stats.govt.nz"

        msg = MIMEMultipart()
        msg['Subject'] = "ICS end to end overnight test"
        msg['From'] = sender
        msg['To'] = recipient
        msg.attach(MIMEText(self.message))
        
        #Add error log file as an attachment
        fil = open(self.folder + self.filename, "rb")
        part = MIMEApplication(fil.read())
        part['Content-Disposition'] = 'attachment; filename="%s"' % self.filename
        msg.attach(part)    
        
        mail = smtplib.SMTP("smtp.gmail.com", 587)
        mail.ehlo()
        mail.starttls()
        mail.login(sender, senderPw)
        mail.sendmail(sender, recipient, msg.as_string())
        mail.quit()



class SalesForceAPI:
    def __init__(self, log):
        self.log = log
        #self.sf = Salesforce(username='ben.schluter@stats.govt.nz.regression', password='sophie22',
                #security_token='XFBTDkhKpVxNXBZ4na81RHxS', sandbox=True)
        self.sf = Salesforce(username='christina.kim@stats.govt.nz', password='Stats12345',
                             security_token='bbNLLmm82AkIjL93evgIztuQ', sandbox=True)        


    def getDacRecords(self):
        #'Id','Name','Access_Code__c','Allocation_Status__c','Document_ID__c','For_Print__c','Is_Non_Private_Dwelling__c','Response__c'
        dacQuery = self.sf.query("\
            SELECT id, Name, access_code__c, allocation_status__c, document_id__c, for_print__c,\
                is_non_private_dwelling__c, response__c \
            FROM DAC_store__c \
            WHERE allocation_status__c = 'Allocated' \
            AND is_non_private_dwelling__c = False" \
            )

        return (dacQuery['records'])


    def getResponse(self, responseId):
        respQuery = self.sf.query_all("\
        SELECT id, name, access_code__c, address__c, address_id__c, collection_code__c, \
            collection_instance__c, collection_mode__c, document_number__c, \
            number_of_dwelling_forms_received__c, number_of_individual_forms_received__c, \
            number_of_occupants__c, Number_of_Individual_Responses_Expected__c,\
            Number_of_Outstanding_Individual_Forms__c, Number_of_Paper_Dwelling_Forms__c, \
            Number_of_Paper_Individual_Forms__c, Mark_In__c \
        FROM Response__c \
        WHERE id = '" + responseId + "'")

        return (respQuery['records'])


    def getResponseFromAccessCode(self, accessCode):
        
        respQuery = self.sf.query_all("\
        SELECT id, name, access_code__c, address__c, address_id__c, collection_code__c, \
            collection_instance__c, collection_mode__c, document_number__c, \
            number_of_dwelling_forms_received__c, number_of_individual_forms_received__c, \
            number_of_occupants__c, Number_of_Individual_Responses_Expected__c,\
            Number_of_Outstanding_Individual_Forms__c, Number_of_Paper_Dwelling_Forms__c, \
            Number_of_Paper_Individual_Forms__c, Mark_In__c \
        FROM Response__c \
        WHERE access_code__c = '" + accessCode + "'")

        return (respQuery['records'])
    

    def checkValidResponse(self, respRecords,dacAccessCode):

        noRespRecords = len(respRecords)

        if (noRespRecords != 1):
            self.log.writeToLog("More than one response store record found - moving onto next record")
            return False    

        noDwellForms = respRecords[0]['Number_of_Dwelling_Forms_Received__c']
        noIndForms = respRecords[0]['Number_of_Individual_Forms_Received__c']
        noOccs = respRecords[0]['Number_of_Occupants__c']
        noIndExpect = respRecords[0]['Number_of_Individual_Responses_Expected__c']
        noOutstandInd = respRecords[0]['Number_of_Outstanding_Individual_Forms__c']
        noPaperDwell = respRecords[0]['Number_of_Paper_Dwelling_Forms__c']
        noPaperInd = respRecords[0]['Number_of_Paper_Individual_Forms__c']
        markIn = respRecords[0]['Mark_In__c']
        accessCode = respRecords[0]['Access_Code__c']
        collectionInstance = respRecords[0]['Collection_Instance__c']

        self.log.writeToLog("Response Store, noDwellForms: " + str(noDwellForms) + ", noIndForms: " + str(noIndForms) + ", noOccs: " + str(noOccs) +
                    ", noIndExpect: " + str(noIndExpect) + ", noOutstandInd: " + str(noOutstandInd) + ", noPaperDwell: " + str(noPaperDwell) +
                    ", noPaperInd: " + str(noPaperInd) + ", markIn: " + str(markIn) + ", accessCode: " + str(accessCode) + ", collectionInstance: " + str(collectionInstance))

        # Check it has not been used
        if (accessCode == dacAccessCode and collectionInstance == "a03P0000004VCiAIAW" and markIn == False
            and (noDwellForms is None or noDwellForms == 0)
            and (noIndForms is None or noIndForms == 0)
            and (noOccs is None or noOccs == 0)
            and (noIndExpect is None or noIndExpect == 0)
            and (noOutstandInd is None or noOutstandInd == 0)
            and (noPaperDwell is None or noPaperDwell == 0)
            and (noPaperInd is None or noPaperInd == 0)):

            return True
        else:
            return False

    def convertInt(self, str):
        value = 0
        try:
            value = int(str)
        except:
            value = 0
        return value
            

    def performSFChecks(self, respRecords):

        self.log.writeToLog("Checking Sales Force Reponse")

        totalForms = len(respRecords)
        if (totalForms != 1):
            self.log.writeToLog("Error - Expected ones SF response record for access code, have: " + str(totalForms) + "\n" + str(respRecords))
        else:
            self.log.writeToLog("Salesforce - Response record present for access code")

        noDwellForms = self.convertInt(respRecords[0]['Number_of_Dwelling_Forms_Received__c'])
        if (noDwellForms != 1):
            self.log.writeToLog("Error - SF: Do not have 1 dwelling form received as expected, have: " + str(noDwellForms) + "\n" + str(respRecords))
        else:
            self.log.writeToLog("Salesforce - One Dwelling form received correctly")
            
        noIndForms = self.convertInt(respRecords[0]['Number_of_Individual_Forms_Received__c'])            
        if (noIndForms != 1):
            self.log.writeToLog("Error - SF: Do not have 1 individual form received as expected, have: " + str(noIndForms) + "\n" + str(respRecords))
        else:
            self.log.writeToLog("Salesforce - One Individual form received correctly")

        noOccs = self.convertInt(respRecords[0]['Number_of_Occupants__c'])
        if (noOccs != 5):
            self.log.writeToLog("Error - SF: Do not have 5 occupants as expected, have: " + str(noOccs) + "\n" + str(respRecords))
        else:
            self.log.writeToLog("Salesforce - Correctly expects five occupants")
  
        noOutstandInd = self.convertInt(respRecords[0]['Number_of_Outstanding_Individual_Forms__c'])
        if (noOutstandInd != 4):
            self.log.writeToLog("Error - SF: Do not have 4 individual responses expected, have: " + str(noOutstandInd) + "\n" + str(respRecords))
        else:
            self.log.writeToLog("Salesforce - Correctly expects four more individual responses")

        noPaperDwell = self.convertInt(respRecords[0]['Number_of_Paper_Dwelling_Forms__c'])
        if (noPaperDwell != 0):
            self.log.writeToLog("Error - SF: Unexpectedly have paper dwelling form: " + str(noPaperDwell) + "\n" + str(respRecords))
        else:
            self.log.writeToLog("Salesforce - Correctly has no paper dwelling forms received")

        noPaperInd = self.convertInt(respRecords[0]['Number_of_Paper_Individual_Forms__c'])
        if (noPaperInd != 0):
            self.log.writeToLog("Error - SF: Unexpectedly have paper individual form: " + str(noPaperInd) + "\n" + str(respRecords))
        else:
            self.log.writeToLog("Salesforce - Correctly has no paper individual forms received")

        markIn = respRecords[0]['Mark_In__c']
        if (markIn != True):
            self.log.writeToLog("Error - SF: Not markedin, stats is: " + str(markIn) + "\n" + str(respRecords))
        else:
            self.log.writeToLog("Salesforce - Reponse correctly marked in")



class Database:
    def __init__(self, log):
        self.log = log
        self.con = None
        self.cur = None

    def connect(self, database):

        try:
            connectString = "DRIVER={SQL Server};SERVER=wuatclsqlcorp10.stats.govt.nz;DATABASE=" + database + ";"
            self.log.writeToLog("Connecting to DB: " + connectString)
            self.con = pypyodbc.connect(connectString)
        except Exception as e:
            self.log.writeToLog("Exception connecting to DB: " + str(e))
            self.log.closeLog()
            sys.exit(9)

    def query(self, sql):

        try:
            self.cur = self.con.cursor()
            self.cur.execute(sql)

            self.columns = [column[0] for column in self.cur.description]
            self.results = []
            for row in self.cur.fetchall():
                self.results.append(dict(zip(self.columns, row)))

            self.cur.close()
        except Exception as e:
            self.log.writeToLog("Exception querying DB:, SQL = " + sql + "\nError: " + str(e))
            self.log.closeLog()
            sys.exit(9)

    def performMarkinChecks(self):

        self.log.writeToLog("Checking Markin table")

        totalForms = len(self.results)
        if (totalForms != 5):
            self.log.writeToLog("Error - Markin: Expecting 5 entries in markin database, have: " + str(totalForms) + "\n" + str(self.results))

        noHouseholdForms = 0
        noDwellingForms = 0
        noIndForms = 0

        for iter in range(len(self.results)):
            formType = self.results[iter]['formtypecode']
            markedIn = self.results[iter]['salesforcemarkinstatuscode']
            noOccs = self.results[iter]['numberofoccupants'] 

            if (formType == "household"):
                noHouseholdForms += 1
            elif (formType == "dwl"):
                noDwellingForms += 1
            elif (formType == "ind"):
                noIndForms += 1

            if (markedIn != "markedIn"):
                self.log.writeToLog("Error - Markin: Record is not marked in, status is: " + markedIn + "\n" + str(self.results[iter]))
            else:
                self.log.writeToLog("Markin: Record is marked in, status: " + markedIn)

            if (formType == "household"):
                if (noOccs != 5):
                    self.log.writeToLog("Error - Markin: Household is not set to 5 occupants, is set to: " + str(noOccs) + "\n" + str(self.results[iter]))
                else:
                    self.log.writeToLog("Markin: Household record correctly present with 5 occupants")
                
        if (noHouseholdForms != 3):
            self.log.writeToLog("Error - Markin: Do not have 3 household form markin records as expected, have: " + str(noHouseholdForms) + "\n" + str(self.results))
        else:
            self.log.writeToLog("Markin: Correctly have three household records")

        if (noDwellingForms != 1):
            self.log.writeToLog("Error - Markin: Do not have 1 dwelling form markin record as expected, have: " + str(noDwellingForms) + "\n" + str(self.results))
        else:
            self.log.writeToLog("Markin: Correctly have 1 dwelling form record")

        if (noIndForms != 1):
            self.log.writeToLog("Error - Markin: Do not have 1 individual form markin record as expected, have: " + str(noIndForms) + "\n" + str(self.results))
        else:
            self.log.writeToLog("Markin: Correctly have 1 individual form record")

    def performResponseStoreChecks(self):

        self.log.writeToLog("Checking Response Store Table")
        totalForms = len(self.results)
        if (totalForms != 5):
            self.log.writeToLog("Error - Reponse Store: Expecting 5 entries in reponse store, have: " + str(totalForms) + "\n" + str(self.results))

        noHouseholdForms = 0
        noDwellingForms = 0
        noIndForms = 0

        for iter in range(len(self.results)):
            instrumentCode = self.results[iter]['instrument_code']
            
            if (instrumentCode == "CEN2018CT2017_Online_Household"):
                noHouseholdForms += 1
            elif (instrumentCode == "CEN2018CT2017_Online_Dwelling"):
                noDwellingForms += 1
            elif (instrumentCode == "CEN2018CT2017_Online_Individual"):
                noIndForms += 1

                               
        if (webEntry != 3):
            self.log.writeToLog("Error - Response Store: Do not have 3 household form records as expected, have: " + str(noHouseholdForms) + "\n" + str(self.results))
        else:
            self.log.writeToLog("Response Store - Correctly have 3 household form records")
        
        if (noDwellingForms != 1):
            self.log.writeToLog("Error - Response Store: Do not have 1 dwelling form record as expected, have: " + str(noDwellingForms) + "\n" + str(self.results))
        else:
            self.log.writeToLog("Response Store - Correctly have 1 dwelling form records")

        if (noIndForms != 1):
            self.log.writeToLog("Error - Response Store: Do not have 1 individual form record as expected, have: " + str(noIndForms) + "\n" + str(self.results))
        else:
            self.log.writeToLog("Response Store - Correctly have 1 individual form records")

    def disconnect(self):
        self.con.close()



###################
# Main class
###################

def replaceDocIDs():
    currUser = os.getlogin()
    outputLog =  "E:\\testing\\Scanning E2E\\"

    log = Logger("ICS_selenium_log",outputLog)
    sf = SalesForceAPI(log)
    webEntry = ''

    # Retrieve 2000 records from the DAC store for Access codes
    dacRecords = sf.getDacRecords()
    iter = 0
    ocIDList = []
    newDocIdList = []
    

    # Go through the DAC codes randomly, finding one which has not been used for ICS or scanning
    while (len(newDocIdList) < 2):
        while (True):
            iter = iter + 1
            log.writeToLog("Using DAC store entry number: " + str(iter))
            # Give up if we haven't found one within the first 2000
            if (iter > 2000):
                log.writeToLog("Can't find a valid access code - giving up")
                log.closeLog()
                sys.exit(9)
            # Select a random code
            i = random.randint(0, len(dacRecords) - 1)
    
            responseId = dacRecords[i]['Response__c']
            dacAccessCode = dacRecords[i]['Access_Code__c']
            log.writeToLog("DAC Store - Response Id: " + str(responseId) + ", Access Code: " + str(dacAccessCode))
            
            # Retrieve the response data from SF for this access code
            respRecords = sf.getResponse(responseId)
    
            isValidResponse = sf.checkValidResponse(respRecords,dacAccessCode)
            # Check it has not been used
            if (isValidResponse):
                newDocIdList.append(dacAccessCode)
                break
    print("newDocIdList: ")
    print(newDocIdList)
    newDocIdList[0] = newDocIdList[0][:len(newDocIdList[0]) - 3]
    newDocIdList[1] = newDocIdList[1][:len(newDocIdList[1]) - 3]
    
  
    return newDocIdList

#docID = replaceDocIDs()
#print(docID)
            
            
            
    


##################################################################################################################
# EmailGeneration.py
##################################################################################################################
# Author: Christina Kim
# Date: 19 June 2017
# Description: Trigger an email notification with error log files as an attachment
##################################################################################################################

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os, os.path
import shutil


def triggerEmails(errorFileList, errorLogPath, subj, sender, recipientList, content, server, port, senderUserName, senderPw):  
    recipientsString = ','.join(recipientList)
    
    #errorFileList = os.listdir(errorLogPath)

    msg = MIMEMultipart()
    msg['Subject'] = subj
    msg['From'] = sender
    msg['To'] = recipientsString
    msg.attach(MIMEText(content))
    
    #Add erro log files as an attachment
    for errorFile in errorFileList or []:
        with open(os.path.join(errorLogPath, errorFile), "rb") as fil:
            part = MIMEApplication(
                    fil.read(),
                )
            part['Content-Disposition'] = 'attachment; filename="%s"' % errorFile
            msg.attach(part)    
    
    
    mail = smtplib.SMTP(server, port)
    mail.ehlo()
    mail.starttls()
    mail.login(senderUserName, senderPw)
    mail.sendmail(sender, recipientList, msg.as_string())
    mail.quit()
    return errorLogPath



# Move the errorLog files to the Emailed folder after an email notification is sent out
def moveFiles(errorFileList, errorLogPath):
    for errorFile in errorFileList:
        if (os.path.isfile(os.path.join(errorLogPath, errorFile))):
            shutil.move(errorLogPath + "\\" + errorFile, errorLogPath + "\\Emailed\\" + errorFile)
    


# This is the main funtion to call the other functions in this module
def generateEmailNotifications(errorLogPath, subj, sender, recipients, message, server, port, senderUserName, senderPw): 
    fileList = os.listdir(errorLogPath)
    errorFileList = []

    #numberOfFiles = len([name for name in fileList if os.path.isfile(os.path.join(errorLogPath, name))])
    
    #Create a list with the error log files
    for name in fileList:
        if os.path.isfile(os.path.join(errorLogPath, name)):
            errorFileList.append(name)
    numberOfFiles = len(errorFileList) 
    #Trigger an email only if there is any error log file generated.
    if (numberOfFiles > 0):
        errorLogPath = triggerEmails(errorFileList, errorLogPath, subj, sender, recipients, message, server, port, senderUserName, senderPw)
        moveFiles(errorFileList, errorLogPath)
   
   


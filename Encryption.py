##################################################################################################################
# Encryption.py
##################################################################################################################
# Author: Christina Kim
# Date: 19 June 2017
# Description: Run the given command line to encrypt files.
# Pre-requisites: 
# - Gpg4win has been installed 
# - The public key has been added to the key ring
# - The public key has been set to be trusted fully.
##################################################################################################################

import subprocess
import os
import shutil

#move zip files from the source location to the target location
def moveFiles(sourceLocation, targetLocation):
   fileList = os.listdir(sourceLocation)
   print("filelist:")
   print(fileList)

   for name in fileList:
      print(name)
      if (name.endswith("gpg")):
         print('gpg')
         shutil.move(sourceLocation + "\\" + name, targetLocation + "current" + "\\" + name)
      else:
         if (name.endswith("zip")):
            print("zip")
            print(sourceLocation + "\\" + name, targetLocation + "processed" + "\\" + name)
            shutil.move(sourceLocation + "\\" + name, targetLocation + "processed" + "\\" + name)
   #subprocess.call(command, shell=True)

# Run the given command line
def encryptFile(sourceFileLocation, targetLocation):
   fileList = os.listdir(sourceFileLocation)
   print(fileList)
   for each in fileList:
      fullFilePath = sourceFileLocation + each
      command = 'gpg --encrypt --recipient cp.uat@stats.govt.nz ' + '"' + fullFilePath + '"'
      subprocess.call(command, shell=True)
   moveFiles(sourceFileLocation, targetLocation)



#fileToZip = 'C:\\Users\\azl-ckim\\Desktop\\CK\\E2E_Scanning\\Scanning Data Files\\'
##Encryption.encryptFile(fileToZip,  'C:\\Users\\azl-ckim\\Desktop\\CK\\E2E_Scanning\\Zipped_Files\\processed\\')

#moveFiles(fileToZip, 'C:\\Users\\azl-ckim\\Desktop\\CK\\E2E_Scanning\\Zipped_Files\\processed\\')


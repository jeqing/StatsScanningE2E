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
   
   print(fileList)
   
   for name in fileList:
      if name.endswith('zip'):
         shutil.move(sourceLocation + "\\" + name, targetLocation + "\\" + name)
   #subprocess.call(command, shell=True)

# Run the given command line
def encryptFile(command, zipFileSourceLocation, zipFileTargetLocation):
   subprocess.call(command, shell=True)
   moveFiles(zipFileSourceLocation, zipFileTargetLocation)

#moveFiles("C:\\Users\\azl-ckim\\Desktop\\CK\\E2E_Scanning\\Zipped_Files", "C:\\Users\\azl-ckim\\Desktop\\CK\\\E2E_Scanning\\Processed_zipped_files")

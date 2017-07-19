##################################################################################################################
# Zipping.py
##################################################################################################################
# Author: Christina Kim
# Date: 19 June 2017
# Description: Generate zip files
##################################################################################################################

import shutil
import zipfile
import os
import datetime
from os.path import basename


def archive(fileToZip):
    shutil.make_archive(fileToZip, 'zip', fileToZip)
          

#Main function in this module
#def archiveFolder(fileToZip):
    #fileListToZip = os.listdir(fileToZip)
    #print(fileListToZip)
    #for each in fileListToZip:
        #fullFilePath = fileToZip + each
        #print("fullpath:" + fullFilePath)
        #if(os.path.isdir(fullFilePath)):
            #archive(fileToZip + each, fileToZip + each)
            

#def archiveFolder(output_filename, fileToZip):
def archiveFolder(fileToZip):
    fileListToZip = os.listdir(fileToZip)

    for file in fileListToZip:
        fullFilePath = fileToZip + "\\" + file
        if(os.path.isdir(fullFilePath)):
            aFile = fileToZip + file + '.zip'
            zippedFile = zipfile.ZipFile(aFile, 'w')
            fullPath = os.path.join(fileToZip, file)
            abs_src = os.path.abspath(fullPath)
            for dirname, subdirs, files in os.walk(fullPath):
                for filename in files:
                    absname = os.path.abspath(os.path.join(dirname, filename))
                    arcname = absname[len(fileToZip):]
                    zippedFile.write(absname, arcname)

                zippedFile.close()
 




#outputFile = 'C:\\Users\\azl-ckim\\Desktop\\CK\\E2E_Scanning\\Zipped_Files\\current\\zipped_files_' + ('{:%Y%m%d_%H%M%S}'.format(datetime.datetime.now()))
#fileToZip = 'C:\\Users\\azl-ckim\\Desktop\\CK\\E2E_Scanning\\Scanning Data Files'

#archiveFolder(outputFile, fileToZip)
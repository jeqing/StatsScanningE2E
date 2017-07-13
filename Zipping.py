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


def archive(output_filename, fileToZip):
    shutil.make_archive(output_filename, 'zip', fileToZip)
          

#Main function in this module
def archiveFolder(fileToZip):
    fileListToZip = os.listdir(fileToZip)
    print(fileListToZip)
    for each in fileListToZip:
        fullFilePath = fileToZip + each
        print("fullpath:" + fullFilePath)
        if(os.path.isdir(fullFilePath)):
            archive(fileToZip + each, fileToZip + each)







#outputFile = 'C:\\Users\\azl-ckim\\Desktop\\CK\\E2E_Scanning\\Zipped_Files\\current\\zipped_files_' + ('{:%Y%m%d_%H%M%S}'.format(datetime.datetime.now()))
#fileToZip = 'C:\\Users\\azl-ckim\\Desktop\\CK\\E2E_Scanning\\Scanning Data Files'

#archiveFolder(outputFile, fileToZip)
##################################################################################################################
# Zipping.py
##################################################################################################################
# Author: Christina Kim
# Date: 19 June 2017
# Description: Generate zip files
##################################################################################################################

import shutil
import zipfile
            

#Main function in this module
def archiveFolder(output_filename, fileToZip):
    shutil.make_archive(output_filename, 'zip', fileToZip)


#def zipFiles(output, fileToZip):       
    #myzip =zipfile.ZipFile(output, 'w')
    #myzip.write(fileToZip)   

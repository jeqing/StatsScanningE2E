##################################################################################################################
# Zipping.py
##################################################################################################################
# Author: Christina Kim
# Date: 19 June 2017
# Description: Generate zip files
##################################################################################################################

import shutil
import zipfile

            
#zfName = 'simonsZip.kmz'
#foo = zipfile.ZipFile(zfName, 'w')
#foo.write("temp.kml")
## Adding files from directory 'files'
#for root, dirs, files in os.walk('files'):
    #for f in files:
        #foo.write(os.path.join(root, f))
#foo.close()
#os.remove("temp.kml")


#Main function in this module
def archiveFolder(output_filename, fileToZip):
    
    shutil.make_archive(output_filename, 'zip', fileToZip)


#def zipFiles(output, fileToZip):       
    #myzip =zipfile.ZipFile(output, 'w')
    #myzip.write(fileToZip)   


outputFile = 'C:\\Users\\azl-ckim\\Desktop\\CK\\E2E_Scanning\\Zipped_Files\\current\\zipped_files_' + ('{:%Y%m%d_%H%M%S}'.format(datetime.datetime.now()))
fileToZip = 'C:\\Users\\azl-ckim\\Desktop\\CK\\E2E_Scanning\\Scanning Data Files'

archiveFolder(outputFile, fileToZip)
import re, sys, os                                                   
import time
import subprocess
   
#http://the.earth.li/~sgtatham/putty/0.52/htmldoc/Chapter6.html
#https://stackoverflow.com/questions/16439039/batch-file-for-putty-psftp-file-transfer-automation
def transferFiles():

    cmd = 'psftp open sftp1.timg.co.nz -l census_test -pw "4#B4&7khCDN&YicG"\n-b C:\\Users\\azl-ckim\\Desktop\\CK\\E2E_Scanning\\batch_script\\batch_script.txt\nls'
    
    subprocess.call(cmd, shell = True)
  


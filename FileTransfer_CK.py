import re, sys, os                                                   
import time
import subprocess
import shutil
   
#http://the.earth.li/~sgtatham/putty/0.52/htmldoc/Chapter6.html
#https://stackoverflow.com/questions/16439039/batch-file-for-putty-psftp-file-transfer-automation

#move encrypted files from the source location to the target location
def moveFiles(sourceLocation, targetLocation):
    fileList = os.listdir(sourceLocation)

    print(fileList)

    for name in fileList:
        shutil.move(sourceLocation + "\\" + name, targetLocation + "\\" + name)
            
def transferFiles():

    #cmd = 'psftp open sftp1.timg.co.nz -l census_test -pw "4#B4&7khCDN&YicG"\n-b C:\\Users\\azl-ckim\\Desktop\\CK\\E2E_Scanning\\batch_script\\batch_script.txt\nls'
    #cmd = 'C:\\Program Files (x86)\\WinSCP\\batch_script2.bat'
    #cmd = '"C:\Program Files\PuTTY\putty.exe" -load ubuntu_vm' 
    
    #Sync Azure VM with AWS Windows VM
    cmd = 'C:\\Program Files (x86)\\WinSCP\\windows_vm_batch_sync.bat'  # Load gpg files to AWS Windows VM
    subprocess.call(cmd, shell = True)
    
    moveFiles('C:\\Users\\azl-ckim\\Desktop\\CK\\E2E_Scanning\\Zipped_Files\\current', 'C:\\Users\\azl-ckim\\Desktop\\CK\\E2E_Scanning\\Zipped_Files\\processed')
    
   
    
    #SSH to AWS Windows VM and run a batch file to sync AWS VM with TIMG sFTP
    #C:\Users\Administrator\Desktop\CK\ScanningE2E\batch_script\batch_move_files_to_timg.bat
    #cmd_ssh = '"C:\\Program Files\\Putty\\putty.exe" Administrator@13.55.178.4 -pw "b7L*(q-heGfd6pa&lgoKm2pgO-DmzlY;"'
    #cmd_ssh = '"C:\\Program Files\\Putty\\putty.exe" -load windows_vm -pw "b7L*(q-heGfd6pa&lgoKm2pgO-DmzlY;"' #use the saved putty session
    
    #subprocess.call(cmd_ssh, shell = True)
  
#transferFiles()
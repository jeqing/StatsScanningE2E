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

# Run the given command line
def encryptFile(command):
   subprocess.call(command, shell=True)


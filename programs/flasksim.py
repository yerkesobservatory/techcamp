#!/usr/bin/env python

''' Flask Server Simulator

    Flask server simulator for Techcamp Balloon project. This
    runs the flask simulator which allows testing communication
    between the flask process and other system components.
    
    Python Version 3
    
    Usage: python flasksim.py configfile.ini
    
    2DO List:
    - Add two way communication to insensim
    - Add one way communication to inphoto for taking rgb image

'''

### Preparation

# Look for parameters
import sys
if len(sys.argv) < 2:
    print("usage: python flasksim.py path/to/config_file.ini")
    exit(1)
# Get config file
import configparser
config = configparser.ConfigParser()
config.read(sys.argv[1])
# Set path is possible
try:
    sys.path.append(config['paths']['pythonpath'])
except:
    pass

# Imports 
import socket
from bparts import commsocket

# Globals
output_port = int(config['ports']['flask_output'])
insense_port = int(config['ports']['flask_insense'])

### Main porgram
cmd = ''
# Main Loop
print("Flask Comm Simulator: type 'help' for help")
while not cmd.lower() in ['exit', 'e', 'x']:
    # Get command
    cmd = input('Enter command to send : ')
    # Print help if requested
    if cmd.lower() in ['h', 'help']:
        print(''' Commands
        - exit (or e, x): to exit
        - target message: to send a message to a target
          valid targets are "output", "insense" and "incam"''')
        continue
    # Run command
    if not cmd.lower().strip() in ['', 'exit', 'e', 'x']:
        # Get target and 
        spaceloc = cmd.find(' ')
        if spaceloc < 0: # if no space is found -> print error
            print("  Error: Can't find 'target message' in command (you need a space between target and message)")
            continue
        target = cmd[:spaceloc]
        message = cmd[spaceloc+1:]
        if target.lower() == 'output':
            commsocket.send_msg(message, output_port)
        elif target.lower() == 'insense':
            response = commsocket.send_recv(message, insense_port)
            print('  Response from InSense: "%s"' % response)
        else:
            print("  Error: '%s' is invalid target" % target)
    
print("That's all Folks!")

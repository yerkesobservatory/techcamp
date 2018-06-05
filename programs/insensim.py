#!/usr/bin/env python

''' Output Server Simulator

    Input server simulator for Techcamp Balloon project. This
    runs the input simulator which allows testing communication
    between the output process and other system components.
    
    Python Version 3
    
    Usage: python outputsim.py configfile.txt

'''

# Look for parameters
import sys
if len(sys.argv) < 2:
    print("usage: python insensim.py path/to/config_file.ini")
    exit(1)
# Get config file
import configparser
config = configparser.ConfigParser()
config.read(sys.argv[1])
# Set path if needed
try:
    sys.path.append(config['paths']['pythonpath'])
except:
    pass

# Imports 
import socket
from bparts import commsocket

# Settings
flask_port = int(config['ports']['flask_insense'])

# Run server with testresponse_noanswer function
commsocket.server(commsocket.testresponse_withanswer, flask_port)
print("InsenseSim - quit")

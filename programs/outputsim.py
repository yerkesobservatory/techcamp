#!/usr/bin/env python

''' Output Server Simulator

    Output server simulator for Techcamp Balloon project. This
    runs the output simulator which allows testing communication
    between the output process and other system components.
    
    Python Version 3
    
    Usage: python outputsim.py configfile.txt

'''

# Imports 
import socket
from bparts import commsocket

# Settings
flask_port = 50747

# Run server with testresponse_noanswer function
commsocket.server(commsocket.testresponse_noanswer, flask_port)

#!/usr/bin/env python

''' Output Server Simulator

    Input server simulator for Techcamp Balloon project. This
    runs the input simulator which allows testing communication
    between the output process and other system components.
    
    Python Version 3
    
    Usage: python outputsim.py configfile.txt

'''

# Imports 
import socket
from bparts import commsocket

# Settings
flask_port = 50748

# Run server with testresponse_noanswer function
commsocket.server(commsocket.testresponse_withanswer, flask_port)
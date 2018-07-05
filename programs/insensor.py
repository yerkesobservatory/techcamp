#!/usr/bin/env python

''' Output Server

    Output server for Techcamp Balloon project. This
    runs the output which regularly gets intput data,
    saves it to a log and serves requests for current
    data.
    
    Python Version 3
    
    Usage: python outputsim.py configfile.txt

    2 Threads:
    * One to take data every 2 sec or so and save to logfile (GetLogData)
    * One to server requests from flask about specific data (DataServer)
    * A dictionary with 'dataname':value will be used to store data (datadict).
    
    2DO:
    K Set up dictionary for "fake" data (make it cputime or random)
    K Set up data reader thread:
      K Set up logging
      K get all data, put into dictionary (should be thread safe)
      K make datafilename formation
      K store all data in logfile with timestamp (filename with datetime)
      K wait until 2s is over
    K Set up two test variables -> run and test
    K Set up flask response thread:
      K server for variable requests --> test it
    * Set up pi and distance sensors
      - connect sensor to pi
      - add to output
      - test in flask
      - make flask pagelet
    * Set up pi and attitude sensors
      - connect sensor to pi
      - add to output
      - test in flask
      - make flask pagelet
      

'''

### Preparation
# Look for parameters
import sys
if len(sys.argv) < 2:
    print("usage: python outputsim.py path/to/config_file.ini")
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
# Get logport
logport = int(config['ports']['logger'])

# Imports 
import os
import time
import socket
from bparts import commsocket
import queue
import threading

# Global Variables
datadict = {'test':0, 'time':'00:00:00'} # The dictionary for the data
datafmt = {'test':'%d', 'time':'%s' } # Formating for the data
datafilename = '' # The filename for the data

### Thread functions

# GetLogData Thread function
def getlogdata():
    """ GetLogData thread function: Runs an infinite loop
        reading all data in specified intervals. Data
        is logged and stored in the dictionary.
    """
    # Get time
    nextime = time.time() + int(config['insense']['datarate'])
    # Infinite loop
    while True:
        # Wait for interval
        count = 0
        while time.time() < nextime:
            time.sleep(0.2)
            count += 1
        nextime = time.time() + int(config['insense']['datarate'])
        commsocket.send_log("Done Waiting, Time=%d, Count=%d" % (nextime, count),
                            logport, 'insensor.getlogdata','DEBUG')
        ### Read all data
        # Time data
        datadict['time'] = time.strftime('%H:%M:%S')
        ### Save data to file
        # Make text line
        s = ''
        for key in datadict:
            s += datafmt[key] % datadict[key]+'\t'
        s.strip()
        # Add to file
        datfile = open(datafilename,'at')
        datfile.write(s+'\n')
        datfile.close()

# DataServer Thread function
def dataserver():
    """ DataServe thread function. Sets up a socket server
        which will respond to incoming data requests
    """
    # start
    commsocket.server(dataserver_responder, int(config['ports']['flask_insense']) )

# DataServer responder function
def dataserver_responder(message):
    """ Returns the requested data
    """
    key = message.strip()
    try:
        value = datafmt[key] % datadict[key]
    except:
        commsocket.send_log("Invalid Value Name %s" % key,
                            logport, 'insensor.dataserver','WARN')
        value = ''
    return value

### Initialize threads_key
# Define data filename (run through time and expandvars)
datafilename = config['insense']['datafile']
datafilename = time.strftime(datafilename)
datafilename = os.path.expandvars(datafilename)
commsocket.send_log('Filename set to %s' % datafilename, logport, 'insensor.setup','INFO')
# Set up threads
getthread = threading.Thread(target = getlogdata)
serverthread = threading.Thread(target = dataserver)
getthread.daemon = True
getthread.start()
serverthread.start()
# Run until servethread shuts down
serverthread.join()



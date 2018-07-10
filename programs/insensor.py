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
import logging
import sys
mpc_on = True
try:
    import Adafruit_GPIO.SPI as SPI
    import Adafruit_MCP3008
except:
    print("WARNING: Couldn't import Adafruit_GPIO or MCP3008 - Analog Inputs will NOT work!")    
    mpc_on = False
bno_on = True
try:
    from Adafruit_BNO055 import BNO055
except:
    print("WARNING: Couldn't import Adafruit_BNO055 - Attitude Sensing will NOT work!")    
    bno_on = False

# Global Variables
datadict = {'test':0, 'time':'00:00:00', # The dictionary for the data
            'analog1':0, 'analog2':0, 'analog3':0, 'analog4':0,
            'analog5':0, 'analog6':0, 'analog7':0, 'analog8':0,
            'heading':0.0, 'pitch':0.0, 'roll':0.0,
            'xgyro':0.0, 'ygyro':0.0, 'zgyro':0.0 }
datafmt = {'test':'%d', 'time':'%s',  # Formating for the data
           'analog1':'%d', 'analog2':'%d', 'analog3':'%d', 'analog4':'%d',
           'analog5':'%d', 'analog6':'%d', 'analog7':'%d', 'analog8':'%d',
           'heading':'%.0f', 'pitch':'%.0f', 'roll':'%.0f',
           'xgyro':'%.2f', 'ygyro':'%.2f', 'zgyro':'%.2f' }
datalist = ['test', 'time', 'analog1', 'analog2', 'analog3', 'analog4',
            'analog5', 'analog6', 'analog7', 'analog7', 'heading',
            'pitch', 'roll', 'xgyro', 'ygyro', 'zgyro']
Nanalog = 8 # Number of analog channels

datafilename = '' # The filename for the data

# AD Converter: Software SPI configuration for MCP3008:
adcCLK  = 22
adcMISO = 23
adcMOSI = 24
adcCS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=adcCLK, cs=adcCS, miso=adcMISO, mosi=adcMOSI)

# Attitude Control: Create and configure the BNO sensor connection
# Raspberry Pi configuration with serial UART and RST connected to GPIO 18:
if bno_on:
    bno = BNO055.BNO055(serial_port='/dev/serial0', rst=18)
    # Initialize the BNO055 and stop if something went wrong.
    if not bno.begin():
        print('Failed to initialize BNO055! Is the sensor connected?')
        bno_on = False
    else:
        # Print system status and self test result.
        status, self_test, error = bno.get_system_status()
        print('BNO055: System status: {0}'.format(status))
        print('        Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
        # Print out an error if system status is in error mode.
        if status == 0x01:
            print('        System error: {0}'.format(error))
            print('        See datasheet section 4.3.59 for the meaning.')

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
        # Analog data
        if mpc_on:
            for i in range(Nanalog):
                aname = 'analog%d' % (i+1)
                try:
                    #mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
                    datadict[aname] = mcp.read_adc(i)
                except Exception as e:
                    commsocket.send_log("Error Reading %s" % aname,
                                        logport, 'insensor.getlogdata','WARN')
                    print(str(e))
                time.sleep(0.05)
        # Attitude control data (BNO055 sensor)
        if bno_on:
            heading, roll, pitch = bno.read_euler()
            datadict['heading'] = heading
            datadict['roll'] = roll
            datadict['pitch'] = pitch
            time.sleep(0.05)
            xgyro, ygyro, zgyro = bno.read_gyroscope()
            datadict['xgyro'] = xgyro
            datadict['ygyro'] = ygyro
            datadict['zgyro'] = zgyro
        ### Save data to file
        # Make text line
        s = ''
        for key in datalist:
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



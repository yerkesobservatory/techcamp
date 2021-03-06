#!/usr/bin/env python

''' Output Server

    Output server for Techcamp Balloon project. This
    runs the output simulator which allows testing communication
    between the output process and other system components.
    
    Python Version 3
    
    Usage: python outputsim.py configfile.txt

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
import time
import socket
from bparts import commsocket
import queue
import threading
import logging
try:
    from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor #Motor HAT
except:
    print("WARNING: Couldn't import Adafruit_MotorHAT - Motor commands will NOT work!")
try:
    import Adafruit_PCA9685 #Servo HAT
except:
    print("WARNING: Couldn't import Adafruit_PCA9685 - Servo commands will NOT work!")

# HAT i2c addresses
motorHatAddr = 0x61
servoHatAddr = 0x40

### Thread functions

# Enqueue Thread function
def enqueue():
    """ Enqueue thread function. Sets up a socket server
        which will put incoming messages on the queue.
    """
    # start 
    print('Starting Enqueue Server:')
    commsocket.server(enqueue_responder, int(config['ports']['flask_output']) )

# Enqueue responder function
def enqueue_responder(message):
    """ Attaches the timestamp to the message and puts it on the queue
    """
    # Generate timestamp (epoch seconds)
    timesec = time.time()
    # Put stamp and message on the queue
    msg = "%f %s" % (timesec, message)
    queue.put(msg)
    # Generate log message
    commsocket.send_log(message, logport, 'output.enqueue', 'DEBUG')

# Executor Thread function
def executor():
    """ Executes commands on the queue with specified time delay.
    """
    # Get time delay
    timedelay = int(config['output']['timedelay'])
    # Loop to get messages
    message = ''
    while not message.strip().lower() in ['x', 'exit', 'q', 'quit']:
        # Get message from queue and split into time and message
        msg = queue.get()
        timesec, message = msg.split(' ', 1)
        timesec = float(timesec)
        commsocket.send_log('Running: %s' % msg, logport, 'output.execute', 'DEBUG')
        # Wait until it's timesec+timedelay
        while time.time() - timesec < timedelay :
            time.sleep(0.5)
        ### EXECUTE MESSAGES HERE
        # Motor:
        if message[0].lower() == 'm': 
            # Make a motor hat with correct number
            mh =Adafruit_MotorHAT(addr=motorHatAddr)
            motor=mh.getMotor(int(message[1]))
            # Get speed, direction and duration
            msplit = message.split()
            speed = int(msplit[1])
            if speed < 0:
                direction = Adafruit_MotorHAT.BACKWARD
                speed = -speed
            elif speed > 0:
                direction = Adafruit_MotorHAT.FORWARD
            else:
                direction = Adafruit_MotorHAT.RELEASE
            duration = float(msplit[2])
            # Set motor movement
            motor.run(direction)
            motor.setSpeed(speed)
            # Wait for duration
            if duration!=0:
                time.sleep(duration)
                motor.run(Adafruit_MotorHAT.RELEASE)
        # Servo
        if message[0] == 's':
            pwm = Adafruit_PCA9685.PCA9685(address=servoHatAddr)
            pwm.set_pwm_freq(60)
            pwm.set_pwm(int(message[1]),0,int(message[3:]))
            time.sleep(1)
        if message[0:5]=='color':
            print("Color Sent")
            incamport=int(config['ports']['flask_incam'])
            commsocket.send_msg(message,incamport)
        commsocket.send_log('Executed: %s' % message, logport, 'output.execute', 'INFO')
    # Sleep a bit to make sure all messages are out and threads can close
    time.sleep(0.2)

# Logging thread function
def logger():
    """ Sets up the logging then starts a
        socket server which logs incoming messages.
    """
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    # Set up logfile - make file handler, formatter and add logger
    logfile = config['output']['logfile']
    fhand = logging.FileHandler(logfile)
    fmt = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    fhand.setFormatter(logging.Formatter(fmt))
    logging.getLogger().addHandler(fhand)
    # Listen for logging events on logport
    print('Starting Logging Server')
    commsocket.server(log_responder, logport )

# Logger responder function
def log_responder(message):
    """ Splits a message of the form loglevel\tlogger\tlogmessage
        and sends it to the logging.
    """
    # Split incoming message
    split = message.split('\t')
    if len(split) < 2:
        lvl = 'INFO'
        lgr = 'Unknown.Sender'
        msg = message
    elif len(split) < 3:
        lvl = split[0]
        lgr = 'Unknown.Sender'
        msg = split[1]
    else:
        lvl = split[0]
        lgr = split[1]
        msg = '\t'.join(split[2:])
    # Get logging level
    if lvl.upper() in ['DEBUG','DEBUGGING']: lvl=logging.DEBUG
    elif lvl.upper() in ['INFO','INFORMATION']: lvl=logging.INFO
    elif lvl.upper() in ['WARN','WARNING']: lvl=logging.WARN
    elif lvl.upper() in ['ERR','ERROR']: lvl=logging.ERROR
    elif lvl.upper() in ['CRIT','CRITICAL']: lvl=logging.CRITICAL
    else: lvl=logging.INFO
    # Log the message
    rec=logging.LogRecord(lgr,lvl,'','',msg,{},{})
    log=logging.getLogger(lgr)
    log.handle(rec)
    return ''

### Initialize threads

# Set up queue
queue = queue.Queue()
# Set up threads
enqthread = threading.Thread(target = enqueue)
execthread = threading.Thread(target = executor)
logthread = threading.Thread(target = logger)
# Program ends when only these threads are active (i.e. execthread is shut down)
enqthread.daemon = True
logthread.daemon = True
# Start threads. At this point the global variables config and queue are set.
enqthread.start()
execthread.start()
logthread.start()
# Run until execthread shuts down
execthread.join()

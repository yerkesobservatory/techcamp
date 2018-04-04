#!/usr/bin/env python

''' Flask Server Simulator

    Flask server simulator for Techcamp Balloon project. This
    runs the flask simulator which allows testing communication
    between the flask process and other system components.
    
    Python Version 3
    
    Usage: python flasksim.py configfile.txt
    
    2DO List:
    - Add two way communication to insensim
    - Add one way communication to inphoto for taking rgb image

'''

### Imports 
import socket

### Functions

# Socket Send
def socksend(port, message):
    ''' Send a message to a given port on localhost
    '''
    # Open socket and connect
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', port))
    s.sendall(message.encode())
    # to receive also data=s.recv(bufsize) # bufsize can be 100 or so
    s.close()
    
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
          valid targets are output, insense and incam''')
        continue
    if not cmd.lower() in ['', 'exit', 'e', 'x']:
        socksend(50747,cmd)
    
print("That's all Folks!")

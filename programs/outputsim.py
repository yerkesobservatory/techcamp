#!/usr/bin/env python

''' Output Server Simulator

    Output server simulator for Techcamp Balloon project. This
    runs the output simulator which allows testing communication
    between the output process and other system components.
    
    Python Version 3
    
    Usage: python outputsim.py configfile.txt

'''

### Imports 
import socket

### Settings
port = 50747
host = 'localhost'

### Main Program
# Make socket, bind and listen
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((host,port))
sock.listen(5)
print('Server Listening (use Ctrl-c to quit)')
# Receive loop
while 1:
    # Get new connection
    conn, addr = sock.accept()
    print('Conected with %s at address %s' % (addr[0],str(addr[1])))
    # Get the message
    reply = conn.recv(1024)
    print('  Got message: %s' % reply)
    # Close the connection
    conn.close()
    print('  Connection Closed')

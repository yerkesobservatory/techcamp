"""
CommSocket
==========

This library contains functions for one- and two-way communication
between different programs over sockets. 

"""

import string
import socket

def send_msg(message, port, server = '127.0.0.1'):
    """ Sends a message to a given port on server. This function
        does a simple socket send without any confirmation.
        
        Arguments:
            message (string): The message to be sent
            port (int): The port to use to send the message
            server (string): The server to send the message to,
                             default is '127.0.0.1'
    """
    # Open socket and connect
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server, port))
    # Send message and close socket
    s.sendall(message.encode())
    s.close()

def send_recv(message, port, server = '127.0.0.1', resplen = 100):
    """ Sends a message to a given port on server. This function
        does a simple socket send without any confirmation, then
        waits for a response which is returned.
        
        Arguments:
            message (string): The message to be sent
            port (int): The port to use to send the message
            server (string): The server to send the message to,
                             (default '127.0.0.1')
            resplen (int): The maximal length of the response,
                           a longer response may be truncated.
                           (default 100)
                           
        Returns:
            If there is a response it is returned as a string.
    """
    # Open socket and connect
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', port))
    # Send message
    s.sendall(message.encode())
    # Wait for response
    resp = s.recv(100)
    resp = resp.decode()
    # Close socket and return
    s.close()
    return resp

def server( respfunct, port):
    """ Sets up server to listen and respond to requests. The
        server needs a response function which is called on each
        incoming message. If respfunct returns a string with
        length > 0 that string is sent back.
        
        Arguments:
            respfunct (function): A function which receives the
                messages as a parameter. It has to return a string
                if the stringlength is > 0 that string is returned.
            port (int): The port to listen to.
            
        Notes:
          - There is no quit: The process needs to be interrupted
            externally (Ctrl-C).
    """
    # Make socket, bind and listen
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost',port))
    sock.listen(5)
    print('Server Listening (use Ctrl-c to quit)')
    # Receive loop
    while 1:
        # Get new connection
        conn, addr = sock.accept()
        print('Conected with %s at address %s' % (addr[0],str(addr[1])))
        # Get the message
        message = conn.recv(1024)
        message = message.decode()
        print('  Got message: %s' % message )
        # Run response function
        response = respfunct(message)
        # Return response
        if response != None:
            conn.sendall( response.encode())
        # Close the connection
        conn.close()
        print('  Connection Closed')

def testresponse_noanswer(message):
    """ Test response function without Answer
    
        Arguments:
            message (str): the incoming message
            
        Returns:
            '', an empty string
    """
    print('Test Response: Received the Message "%s"' % message)
    return ''
    
def testresponse_withanswer(message):
    """ Test response function with Answer
        
        Arguments:
            message (str): the incoming message
            
        Returns:
            A string with the message and confimation
    """
    print('Test Response: Recieved the Message "%s"' % message)
    return "OK: " + message

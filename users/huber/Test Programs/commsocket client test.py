import socket
from bparts import commsocket
from time import sleep
import shutil
import threading

# Globals
flask_port = 50747
cmd = ''
message=' '

def resp_funct(message):
	print message
	return message

commsocket.server(resp_funct, flask_port)

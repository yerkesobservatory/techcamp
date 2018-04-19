# Imports 
from flask import render_template, request
from app import app
from app.forms import commandForm
import socket
from bparts import commsocket

# Globals
output_port = 50747
insense_port = 50748

#Routes for Flask --Basicly the web address for Flask
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/server', methods=['GET','POST'])
def server():
	#Gets the form data from the website
	form=commandForm(request.form)
	if request.method == 'POST':
		command = form.command.data

		spaceloc = command.find(' ')
		if spaceloc < 0: # if no space is found -> print error
		    print("  Error: Can't find 'target message' in command (you need a space between target and message)")
		target = command[:spaceloc]
		message = command[spaceloc+1:]
		if target.lower() == 'output':
		    commsocket.send_msg(message, output_port)
		elif target.lower() == 'insense':
		    response = commsocket.send_recv(message, insense_port)
		    print('  Response from InSense: "%s"' % response)
		else:
		    print("  Error: '%s' is invalid target" % target)



	return render_template('server.html',title='Send Command',form=form)

# Imports for config and bparts
import configparser
import io
import sys
config = configparser.ConfigParser()
#Reads the master.ini config file in the configs folder
config.read('../configs/master.ini')
#Takes the techcamp folder path from the master.ini config file
techcamp_path = config['paths']['pythonpath']
#Adds the techcamp folder as a system path so that is can find bparts
sys.path.append(techcamp_path)
from bparts import commsocket

# Imports 
from flask import render_template, request
from app import app
from app.droneterm import commandForm
from app.cameracontrol import cameraForm
from app.motorcontrol import submitForm, mpForm, mtForm, servoForm
import socket
from bparts import commsocket

# Globals
output_port = 50747
insense_port = 50748

#Functions
def send_command(command):
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


#Routes for Flask --Basicly the web address for Flask
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/droneterm', methods=['GET','POST'])
def droneterm():
	#Gets the form data from the website
	form=commandForm(request.form)
	if request.method == 'POST':
		send_command(form.command.data)

	return render_template('droneterm.html',title='Send Command',form=form)
@app.route('/stream')
def stream():
	return render_template('stream.html')
@app.route('/color')
def color():
	return render_template('color.html')
@app.route('/camera',methods=['GET','POST'])
def camera():
	form=cameraForm(request.form)
	if request.method == 'POST':
		if form.takeimg.data == 1:
			send_command('incam color')
			print 'sent incam color'
	return render_template('camera.html',form=form)
@app.route('/motor',methods=['GET','POST'])
def motor():
	submit=submitForm(request.form)
	mp=mpForm(request.form)
	mt=mtForm(request.form)
	servo=servoForm(request.form)
	if request.method == 'POST':
		print('POST')
	return render_template('motorcontrol.html',submit=submit,mp=mp,servo=servo,mt=mt)


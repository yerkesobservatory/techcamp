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
from flask import render_template, request, flash
from app import app
from app.droneterm import commandForm
from app.cameracontrol import cameraForm
from app.motorcontrol import submitForm, mpForm, mtForm, motorForm
import socket
from bparts import commsocket

# Globals
output_port = 50749
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
			print('sent incam color')
	return render_template('camera.html',form=form)
@app.route('/motor',methods=['GET','POST'])
def motor():
	submit=submitForm(request.form)
	mp=mpForm(request.form)
	mt=mtForm()
	motor=motorForm()
	if request.method == 'POST':

		validator=[0,0,0]
		#Gets the data from the inputs
		power=mp.power.data
		time=mt.time.data
		motorSet=int(motor.motor.data)

		#Checks is the motor power input was valid
		if -255<=power<=255:
			flash("Power set for (%d)"%power)
			validator[0]=1
		else:
			flash("Power outside of range(-255,255)")
		#Checks if the time input was valid
		if -1<=time<=1:
			flash("Time set for (%f)"%time)
			validator[1]=1
		else:
			flash("Time outside of range(-1,1)")

		#Check what motors were selected
		if motorSet == 0:
			flash("Please Select a Motor")
		elif motorSet == 1:
			flash("Motor 1 selected")
			validator[2]=1
		elif motorSet == 2:
			flash("Motor 2 selected")
			validator[2]=1
		elif motorSet == 3:
			flash("Both Motors selected")
			validator[2]=1

		#checks validators
		if all(i == 1 for i in validator):
			flash("It Worked")
			flash(("Sent command 'output m{0} {1:03} {2}'").format(motorSet,power,time))
			send_command(("output m{0} {1:03} {2}").format(motorSet,power,time))
		else:
			flash("Message not sent, check errors")

	return render_template('motorcontrol.html',submit=submit,mp=mp,motor=motor,mt=mt)


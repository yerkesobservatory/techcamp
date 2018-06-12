#!/usr/bin/python
"""
Before using this program, you must follow the instructions on this page:
https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi/installing-software
"""
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
from time import sleep
message = 'mp1 255'

def gopher(message):


	if message[0:2] == 'mp':
		# Initialze
		mh = Adafruit_MotorHAT(addr=0x62)

		# Get motor
		motor = mh.getMotor(int(message[2]))

		#Get direction and speed
		dirSpeed = message[4:]
		if dirSpeed[0] == '-':
			direction = Adafruit_MotorHAT.BACKWARD
			speed = int(dirSpeed[1:])
		elif dirSpeed[0] == '0':
			direction = Adafruit_MotorHAT.RELEASE
			speed = 0
		else:
			direction = Adafruit_MotorHAT.FORWARD
			speed = int(dirSpeed)

		# Set direction
		motor.run(direction)

		#Set speed
		motor.setSpeed(speed)


	if message[0:2] == 'mt':
		# Initialze
		#from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
		mh = Adafruit_MotorHAT(addr=0x62)

		# Get motor
		motor = mh.getMotor(int(message[2]))

		#Get direction and time
		dirTime = message[4:]
		if dirTime[0:2] == '-1':
			direction = Adafruit_MotorHAT.BACKWARD
			time = int(dirTime[3:])

		elif dirTime[0] == '1':
			direction = Adafruit_MotorHAT.FORWARD
			time = int(dirTime[2:])

		# Set direction
		motor.run(direction)

		# Run for time
		motor.setSpeed(255)
		sleep(time)
		motor.run(Adafruit_MotorHAT.RELEASE)
		motor.setSpeed(0)
gopher(message)

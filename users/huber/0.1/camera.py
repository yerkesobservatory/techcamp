# Imports 
import socket
from bparts import commsocket
import picamera
from time import sleep
from datetime import datetime
import shutil


camera = picamera.PiCamera()
# Globals
flask_port = 50748
cmd = ''
message=''
def img_stream():
	sleep(1)
	#Change camera settings	
	camera.color_effects = (128,128) #sets the camera to black and white
	camera.resolution(320,240) #sets the resolution of the camera
	camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S') #adds time stamp to image

	camera.capture('app/static/images/image.jpg') #Take the image
	
	shutil.copy('image.jpg', 'image2018-04-15_15-32-26.jpg')

def take_color():
	#Change camera settings	
	camera.color_effects = None #removes all color effects
	camera.resolution(2592,1944)  #sets the resolution of the camera
	camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S') #Adds time stamp to image

	camera.capture('app/static/images/color2018-04-15_15-32-26.jpg') #Take the image

# Main Loop
while 1:
	img_stream()
	
	#Listen to the flask socket; Removed 4/18/18 due to respfunct error
	#commsocket.server(answer(), flask_port)

	#consantly create a image in the image folder for Flask
	camera.capture('app/static/images/image.jpg')



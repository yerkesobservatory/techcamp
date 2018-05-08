# Imports 
import socket
from bparts import commsocket
import picamera
from time import sleep
from datetime import datetime
import shutil
import threading

camera = picamera.PiCamera()
# Globals
flask_port = 50747
cmd = ''
message=''
time=0
def img_stream(time):
	while 1:
		sleep(1)
		#Change camera settings	
		camera.color_effects = (128,128) #sets the camera to black and white
		camera.resolution=(320,240) #sets the resolution of the camera
		camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S') #adds time stamp to image

		camera.capture('app/static/images/stream.jpg') #Take the image
		print 'Img taken'
		if time==10:
			camera.capture('data/images/bw/bw_'+datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+'.jpg')
			time=0
		time = time+1
		#shutil.copy('image.jpg', 'image2018-04-15_15-32-26.jpg')

def take_color(message):
	print message
	if message == 'color':
	#Change camera settings	
		camera.color_effects = None #removes all color effects
		camera.resolution=(2592,1944)  #sets the resolution of the camera
		camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S') #Adds time stamp to image
		camera.capture('app/static/images/color.jpg') #Take the image
		camera.capture('data/images/color/color_'+datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+'.jpg')

def commsocket_funct():
	print 'Starting Commsocket'
	commsocket.server(take_color, flask_port)

# Main Loop
x = threading.Thread(name='img_stream', target=img_stream,args=(time,))
y = threading.Thread(name='socket', target=commsocket_funct)
print 'starting now'
x.start()
y.start()

	#Listen to the flask socket; Removed 4/18/18 due to respfunct error
	#commsocket.server(answer(), flask_port)

	#consantly create a image in the image folder for Flask




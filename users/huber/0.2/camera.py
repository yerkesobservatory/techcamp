import picamera
camera = picamera.PiCamera()
while true:
	#consantly create a image in the image folder for Flask
	camera.capture('app/static/images/image.jpg')

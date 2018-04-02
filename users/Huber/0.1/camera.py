import picamera
camera = picamera.PiCamera()
while true:
	camera.capture('app/static/images/image.jpg')

#importing package
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

#Camera Initialization and capture refrance
camera = PiCamera()
camera.resolution=(640,480)
camera.framerate=32
rawCapture = PiRGBArray(camera)

#Camera Warm Up
time.sleep(0.1)

##capture image (All Open CV images must be in BGR format)
#camera.capture(rawCapture, format="bgr")
#image = rawCapture.array

#capture frames from camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port="True"):
	image=frame.array
	#Show the frame
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xff
	#clear the stream in preparation for next frame
	rawCapture.truncate(0)

	#if 'q' break loop
	if key == ord("q"):
		break
	#delay frames
	#time.sleep(.05)

#dispay the image on screen and wait for keypres
#cv2.imshow("Image", image)
#cv2.waitKey(0)


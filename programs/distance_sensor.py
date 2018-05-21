# import libraries
import RPi.GPIO as GPIO
import time


while True:
        
    # setup pins
    GPIO.setmode(GPIO.BCM)
    TRIG = 23
    ECHO = 24

    # initialize sensor
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(TRIG, GPIO.IN)
    GPIO(TRIG, False)
    time.sleep(2)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # send pulse
    while GPIO.input(ECHO) == 0:
	pulse_start = time.time()

    # recieve pulse	
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
	
    # calculate distance
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    # record distance in file
    with open('distance.txt', 'w') as f:
        f.write(str(distance))
	
    # reset pins
    GPIO.cleanup()

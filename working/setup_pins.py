
import os, os.path, glob, time, sys, datetime, smtplib

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
for pin in [6]:
	print "Setting pin ",pin, " high"
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, GPIO.HIGH)


device_folder = glob.glob('/sys/bus/w1/devices/28*')

print "device_folder is:"
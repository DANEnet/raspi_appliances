# this file is adapted from http://jartweb.net/blog/wp-content/uploads/2013/12/Raspberry-Pi-Logger-with-LCD.pdf

import os, os.path, glob, time, sys, datetime, smtplib
global device_file

# define some globals
sendEmails = True   # send email when tolerance is exceeded or error occurs
alertMaximum = 35   # max temperature (C) before alerting
alertMinimum = 5    # min temperature (C) before alerting
maxTry = 1000       # number of tries before it gives up and sends an email

from get_temp_2wire import *
from plot_temp_date import *
# get the location of the DS18B20 in the system

device_folder = glob.glob('/sys/bus/w1/devices/28*')
device_file = device_folder[0] + '/w1_slave'

print "monitor_server: device_file",device_file

# this is the top of the real program
outfilename="readings"+time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
OUTFILE = open(outfilename, "w")

while 1:
    temp = read_2wire_temp() #get the temp
    output_str = "%s, %f3.2 C, %f3.3 F\n"%(time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()),
                                          temp, (temp*1.800 + 32))
    print output_str
    OUTFILE.write(output_str)
    OUTFILE.flush()
    time.sleep(60*5)

if os.path.exists('error_log.txt'): # if we have an active error
    sendEmails = False              # don't send another email

if (temp == -999):
    if(sendEmails):
        sendEmailSMTP('sensor error')

elif (temp < alertMinimum):
        if(sendEmails):
            sendEmailSMTP('low temperature alert')

elif (temp > alertMaximum):
        if(sendEmails):
            sendEmailSMTP('high temperature alert')
else:
    print('T1:'+str(temp))
    if(not sendEmails):        # since we got a valid answer delete the error log
        os.remove('error_log.txt')


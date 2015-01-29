# this file is adapted from http://jartweb.net/blog/wp-content/uploads/2013/12/Raspberry-Pi-Logger-with-LCD.pdf

import os, os.path, glob, time, sys, datetime, smtplib
global device_file

# define some globals
sendEmails = True   # send email when tolerance is exceeded or error occurs
alertMaximum = 35   # max temperature (C) before alerting
alertMinimum = 5    # min temperature (C) before alerting
maxTry = 1000       # number of tries before it gives up and sends an email

from get_temp_1wire import *
from plot_temp_date import *
# get the location of the DS18B20 in the system

device_folder = glob.glob('/sys/bus/w1/devices/28*')
device_file = device_folder[0] + '/w1_slave'

def check_alert(reading_in): #This is an iterator so variables are constant
    
    for dat in reading_in:    
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

                
        yield dat  # this makes this function an iterator






######################################
# this is the top of the real program
######################################

device_folder = glob.glob('/sys/bus/w1/devices/28*')
device_file = device_folder[0] + '/w1_slave'

print "monitor_server: device_file",device_file


outfilename="/var/www/readings"+time.strftime("%Y-%m-%d", time.localtime())
OUTFILE = open(outfilename, "w")

ONEDAY = 24*60*60
PLOT_INT = 15*60
last_housekeeping = time.time() - ONEDAY  #force first pass to trigger
last_plot = time.time() - ONEDAY  #force first pass to trigger
#print time.time(), type(time.time)
#last_day = time.strftime("%Y-%m-%d", time.localtime()-ONEDAY)
readings = []
dates = []


while 1:
    reading = read_1wire_temp(device_file) #get the temp
    readings.append(reading)
    dates.append(datetime.datetime.now())
    
    output_str = "%s, %6.3f\n"%(time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()),
                                           (reading*1.800 + 32))
    print output_str
    OUTFILE.write(output_str)
    OUTFILE.flush()
    check_alert(reading)

    
    today_str=time.strftime("%Y-%m-%d", time.localtime())
    if (time.time() - last_plot) > PLOT_INT: 
        plotdata(dates, readings, "/var/www/plot"+today_str)
    
    if (time.time() - last_housekeeping > ONEDAY): # and (today > last_day):
        # daily tasks
        readings=[]
        dates = []
        last_day = today_str
        last_housekeeping = time.time()
        outfilename="/var/www/readings"+time.strftime("%Y-%m-%d", time.localtime())
        OUTFILE.close()
        OUTFILE = open(outfilename, "w")
    
    time.sleep(60*5)


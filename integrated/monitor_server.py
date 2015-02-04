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
import send_email 
# get the location of the DS18B20 in the system

device_folder = glob.glob('/sys/bus/w1/devices/28*')
device_file = device_folder[0] + '/w1_slave'

def get_reading(device_file):
    reading_c = read_1wire_temp(device_file) #get the temp
    reading_f = reading_c*1.800 +32 #Change to farenheight
    return reading_c, reading_f
    



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


text_outfilename="/var/www/readings"+time.strftime("%Y-%m-%d", time.localtime())+".csv"
today_str=time.strftime("%Y-%m-%d", time.localtime())
last_plot_name = "/var/www/plot"+today_str+".png"
OUTFILE = open(text_outfilename, "a") # lets append rather than truncate if it already exists

ONEDAY = 24*60*60
PLOT_INT = 5*60
last_housekeeping = time.time() - ONEDAY  #force first pass to trigger
last_plot = time.time() - ONEDAY  #force first pass to trigger by setting lat plot to one day ago"
#print time.time(), type(time.time)
yesterday = datetime.datetime.today()-datetime.timedelta(days=1)
last_day = yesterday.strftime("%Y-%m-%d")
readings_f = []
dates = []

###########################################
#This is the main loop which cycles forever
###########################################

while 1:
    reading_c, reading_f = get_reading(device_file) 
    readings_f.append(reading_f)
    dates.append(datetime.datetime.today())
    
    output_str = "%s, %6.3f, %6.3f\n"%(time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()),
                                           reading_f, reading_c)
    print output_str
    OUTFILE.write(output_str)
    OUTFILE.flush()
    check_alert(reading_f)

    
    today_str=time.strftime("%Y-%m-%d", time.localtime())
    
    print "today_str:", today_str
    print "last_day: ", last_day


    #### At the end of the day reset things
    if (today_str > last_day):
        # daily tasks - Do this when day changes.
        attachmentFilePaths = [last_plot_name, text_outfilename ]
        now = datetime.datetime.today()
        send_email.sendMail("Test message from server %s"%now.strftime("%Y-%m-%dT%H:%M:%S"),
             "the readings go here %s"%now.strftime("%Y-%m-%dT%H:%M:%S"),
             *attachmentFilePaths)

        
        readings_f=readings_f[:0]
        dates = dates[:0]
        last_day = today_str
        last_housekeeping = time.time()
        OUTFILE.close()
        
        text_outfilename="/var/www/readings"+time.strftime("%Y-%m-%d", time.localtime())+".csv"
        OUTFILE = open(text_outfilename, "a") # again append if exists
        today_str=time.strftime("%Y-%m-%d", time.localtime())


       ##### Do a plot every so often    
    if (time.time() - last_plot) > PLOT_INT:
        #do not putout an empty graph at the start of the day
        if len(readings_f) == 0:
            reading_c, reading_f = get_reading(device_file)
            readings_f.append(reading_f)
            dates.append(datetime.datetime.today())
            time.sleep(60*2)
            reading_c, reading_f = get_reading(device_file)
            readings_f.append(reading_f)
            dates.append(datetime.datetime.today())

        last_plot_name = "/var/www/plot"+today_str+".png"
        plotdata(dates, readings_f, last_plot_name)
        last_plot = time.time()
        #overwrites all day then goes on to new day

      
    
    time.sleep(60*2)


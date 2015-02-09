# this file is adapted from http://jartweb.net/blog/wp-content/uploads/2013/12/Raspberry-Pi-Logger-with-LCD.pdf

import os, os.path, glob, time, sys, datetime, smtplib
global device_file

# define some globals
serverLocation = "CSCI "
sendEmails = True   # send email when tolerance is exceeded or error occurs
alertMaximum = 85   # max temperature (F) before alerting
alertMinimum = 35    # min temperature (F) before alerting
maxTry = 1000       # number of tries before it gives up and sends an email
ONEDAY = 24*60*60
PLOT_INT = 5*60
SAMPLE_PERIOD = 2*60

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
    

def get_statistics(readings):
  readings.sort()
  min = readings[0]
  max = readings[-1]
  median = readings[int(len(readings)/2)]
  return min, max, median
    

def check_alert(reading_in_f ): #This is an iterator so dates preserve between constants
    
    last_alert = datetime.datetime.today()-datetime.timedelta(days=1).timestamp()
        ## start more than one day ago
    
    for dat in reading_in:
        today = datetime.datetime.today().timestamp()
        error_str = ""  ## clear each time through loop

        if (temp == -999):
            if(today - last_alert) > ONEDAY:
                error_str = 'sensor error'

        elif (temp < alertMinimum):
            if(today - last_alert) > ONEDAY:
                error_str = "low temperature alert"

        elif (temp > alertMaximum):
             if(today - last_alert) > ONEDAY:
                error_str='high temperature alert'
                    
        else: ## Server is OK
            print('T1:'+str(temp))
            continue  ## get a new data point
            

        message_subject = "ERROR from server %s %s at %s"% (serverLocation,
                                                         error_str,
                                                         serverLocation+now.strftime("%Y-%m-%dT%H:%M:%S")
        message_body = "\n\nMin Temp was: %6.2f F\n Max Temp was: %6.2f F\n Median Temp was: %6.2f F \n"%get_statistics(readings)  ## min, max, median
        send_email.sendMail(message_subject,
             now.strftime("%Y-%m-%dT%H:%M:%S")+message_body,
             attachmentFilePaths)
       
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


    #### At the end of the day reset things send email
    if (today_str > last_day):
        # daily tasks - Do this when day changes.
        #attachmentFilePaths = [last_plot_name, text_outfilename ]
        attachmentFilePaths = [last_plot_name] # raw csv data getting encoded
        now = datetime.datetime.today()

        message_subject = "Update from server %s"% serverLocation+now.strftime("%Y-%m-%dT%H:%M:%S"
        message_body = "\n\nMin Temp was: %6.2f F\n Max Temp was: %6.2f F\n Median Temp was: %6.2f F \n"%get_statistics(readings)  ## min, max, median
        send_email.sendMail(message_subject,
             now.strftime("%Y-%m-%dT%H:%M:%S")+message_body,
             attachmentFilePaths)

        
        readings_f=readings_f[0:0]
        dates = dates[0:0]
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
            time.sleep( SAMPLE_PERIOD)
            reading_c, reading_f = get_reading(device_file)
            readings_f.append(reading_f)
            dates.append(datetime.datetime.today())

        last_plot_name = "/var/www/plot"+today_str+".png"
        plotdata(dates, readings_f, last_plot_name)
        last_plot = time.time()
        #overwrites all day then goes on to new day

      
    
    time.sleep( SAMPLE_PERIOD)


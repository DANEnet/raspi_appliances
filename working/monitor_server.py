# this file is adapted from http://jartweb.net/blog/wp-content/uploads/2013/12/Raspberry-Pi-Logger-with-LCD.pdf

import os, os.path, glob, time, sys, datetime, smtplib
global device_file

# define some globals
ONEDAY = 24*60*60


from get_temp_1wire import *
from plot_temp_date import *
import send_email 
import get_config

config = get_config.get_config()

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
    

def check_4_alert(reading_in_f ): #This is an iterator so dates preserve between constants
    #global readings_f # [remove this is kludge maybe should be a class]
    last_alert = datetime.datetime.today()-datetime.timedelta(days=1).timestamp()
        ## start more than one day ago
    print "ChecK_alter info", reading_in_f
    for dat in reading_in_f:
        print "Check_4_alert_info loop: ", dat, last_alert
        today = datetime.datetime.today().timestamp()
        error_str = ""  ## clear each time through loop

        if (dat == -999):
            if(today - last_alert) > ONEDAY:
                error_str = "sensor error"

        elif (dat < alertMinimum):
            if(today - last_alert) > ONEDAY:
                error_str = "low temperature alert"

        elif (dat > alertMaximum):
             if(today - last_alert) > ONEDAY:
                error_str='high temperature alert'
                    
        else: ## Server is OK
            print('T1:'+str(dat))
            continue  ## get a new data point
            

        error_subject = "ERROR from server %s %s at %s"% (serverLocation,
                                                         error_str,
                                                         serverLocation+now.strftime(" %Y-%m-%dT%H:%M:%S"))
        #error_body =  ("""\n\nMin Temp was: %6.2f F
        #                Max Temp was: %6.2f F\n
        #                Median Temp was: %6.2f F \n"""%
        #                get_statistics(readings_f))  ## min, max, median

        error_body = "Temperature is: %6.2f"% reading_in_f                                                   
        send_email.sendMail(error_subject,
             now.strftime("%Y-%m-%dT%H:%M:%S")+error_body,
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

yesterday = datetime.datetime.today()-datetime.timedelta(days=1)
last_day = yesterday.strftime("%Y-%m-%d")
last_clearance  = datetime.datetime.today()

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
    
    today_str=time.strftime("%Y-%m-%d", time.localtime())
    
    print "today_str:", today_str
    print "last_day: ", last_day


    #### At the end of the day reset things
    if (today_str > last_day):
        # daily tasks - Do this when day changes.
        #attachmentFilePaths = [last_plot_name, text_outfilename ]
        if os.path.isfile(last_plot_name):       # do not try to attach if it does not exist
          attachmentFilePaths = [last_plot_name] # raw csv data getting encoded
        else:
          attachmentFilePaths = []
        last_clearance = now = datetime.datetime.today()

        message_subject = "Update from server %s"% config["serverLocation"]+now.strftime("%Y-%m-%dT%H:%M:%S")
        message_body = """\n\nMin Temp was: %6.2f F
Max Temp was: %6.2f F
Median Temp was: %6.2f F """%get_statistics(readings_f)  ## min, max, median
#        send_email.sendMail(message_subject,
#             now.strftime("%Y-%m-%dT%H:%M:%S")+message_body,
#             attachmentFilePaths)

        
        readings_f=readings_f[0:0]
        dates = dates[0:0]
        print "after truncate lengths: ", len(readings_f), len(dates) 
        last_day = today_str
        last_housekeeping = time.time()
        OUTFILE.close()
        
        text_outfilename="/var/www/readings"+time.strftime("%Y-%m-%d", time.localtime())+".csv"
        OUTFILE = open(text_outfilename, "a") # again append if exists
        today_str=time.strftime("%Y-%m-%d", time.localtime())


       ##### Do a plot every so often    
    if (time.time() - last_plot) > config["PLOT_INT"]:
        #do not putout an empty graph at the start of the day
        while len(readings_f) < 2:  ## get 2 readings for at least some kind of graph.
            time.sleep(config["SAMPLE_PERIOD"])
            reading_c, reading_f = get_reading(device_file)
            readings_f.append(reading_f)
            dates.append(datetime.datetime.today())
            

        last_plot_name = "/var/www/plot"+today_str+".png"
        plotdata(dates, readings_f, last_plot_name)
        last_plot = time.time()
        #overwrites all day then goes on to new day

   
    temp = check_4_alert(reading_f)# check and potentialy send email after plot
      
    
    time.sleep(config["SAMPLE_PERIOD"])


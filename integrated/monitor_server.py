# this file is adapted from http://jartweb.net/blog/wp-content/uploads/2013/12/Raspberry-Pi-Logger-with-LCD.pdf

import os, os.path, glob, time, sys, datetime, smtplib

# define some globals
sendEmails = True   # send email when tolerance is exceeded or error occurs
alertMaximum = 35   # max temperature (C) before alerting
alertMinimum = 5    # min temperature (C) before alerting
maxTry = 1000       # number of tries before it gives up and sends an email

from get_temp_2wire include *
from plot_temp_date include *



# this is the top of the real program

temp = read_temp() #get the temp

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


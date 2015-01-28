# this file is adapted from http://jartweb.net/blog/wp-content/uploads/2013/12/Raspberry-Pi-Logger-with-LCD.pdf

import os, os.path, glob, time, sys, datetime, smtplib

# define some globals
sendEmails = True   # send email when tolerance is exceeded or error occurs
alertMaximum = 35   # max temperature (C) before alerting
alertMinimum = 5    # min temperature (C) before alerting
maxTry = 1000       # number of tries before it gives up and sends an email

# get the location of the DS18B20 in the system
device_folder = glob.glob('/sys/bus/w1/devices/28*')
device_file = device_folder[0] + '/w1_slave'

def sendEmailSMTP(message='test'):         # utility that sends the alerts
    smtpServer = 'SMTP.gmail.com'          # SMTP email server
    username = 'me@gmail.com'              # SMTP server login, if needed
    password = 'password'                  # SMTP server login, if needed
    From = 'me@gmail.com'                  # the from email field
    To = ['who@gmail.com']                 # the to email field
    Date = time.ctime(time.time())
    Subject = 'Server temperature - ALERT'
    Text = message

    # format the message into a string
    myMessage = ('From: %s\nTo: %s\nDate: %s\nSubject: %s\n%s\n' %(From, To, Date, Subject, Text))

    # make a log file (this is how we will know an error was found in the previous call)
    f = open('error_log.txt', 'r')
    f.write(Text)
    f.close()

    # connect and log into the server
    s = smtplib.SMTP(smtpServer)          # intitialize the server
    try:
        s.login(username, password)       # try to login
    except:
        print 'SMTP login error'          # trap the login error

    #send the message
    try:
        s.sendmail(From, To, myMessage)  # try send message
    except:
        print 'Error Sending Message'    # trap the send message error
    finally:
        s.quit()                         # close the connection

def read_temp_raw(): # function that grabs the raw temperature data from the sensors
    f = open(device_file, 'r') # the sensor appears as a file
    lines = f.readlines()      # this is a list of two lines
    f.close()
    return lines

def read_temp(): # function that checks that the connection was good and pulls out the temperature
    lines = read_temp_raw()
    numTry = 0
    while lines[0].strip()[-3:] != 'YES' and numTry < maxTry: # loop until we get a valid response
        time.sleep(0.5)
        lines = read_temp_raw()  # try again
        numTry += 1

    if numTry != maxTry:                   # if we have not exceeded maxTry
        equals_pos = lines[1].find('t=')
        temp = float(lines[1][equals_pos+2:])/1000
    else:
        temp = -999                       # make a bad value to indicate error

    return temp


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
    print('T1: '+str(temp))
    if(not sendEmails):        # since we got a valid answer delete the error log
        os.remove('error_log.txt')


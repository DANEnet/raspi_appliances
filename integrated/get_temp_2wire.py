# this file is adapted from http://jartweb.net/blog/wp-content/uploads/2013/12/Raspberry-Pi-Logger-with-LCD.pdf

import os, os.path, glob, time, sys, datetime

maxTry = 1000       # number of tries before it gives up on reading

def read_temp_raw(): # function that grabs the raw temperature data from the sensors
    f = open(device_file, 'r') # the sensor appears as a file
    lines = f.readlines()      # this is a list of two lines
    f.close()
    return lines

def read_2wire_temp(): # function that checks that the connection was good and pulls out the temperature
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

main():
  global maxTry
  maxTry = 1000       # number of tries before it gives up on reading
  print read_2wire_temp()

if __name__ == "__main__":
    main()
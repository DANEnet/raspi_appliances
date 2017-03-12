import time, datetime, re
import numpy as np
import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab! or get no display errors
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.image as mpimg
import get_config



def plotdata(dates, readings_f, infilename, outfilename):
  #days, temp_f = np.loadtxt("/home/pi/server_monitor/temps2015-01-01T10:09:44", unpack=True,
  #        converters={ 0: mdates.strpdate2num('%Y-%m-%dT%H:%M:%S')})


  #this is a cowardly way of testing reading plot data from file rather than
  #passing it from the in memory array
  #designed so that if it is commmented out 
  dates = []
  readings_f = []
  INFILE = open(infilename, "r")
  for line in INFILE:
    ln_date, ln_tempf, ln_tempc = re.split(r",\w*", line)
    dates.append(datetime.datetime.strptime(ln_date, "%Y-%m-%dT%H:%M:%S"))
    readings_f.append(float(ln_tempf))
    #print "read in", dates[-1],"temp",readings_f[-1], line
    
  #end of test on reading file

  print "in plotdata length readings_f: ", len(readings_f)
  print "in plotdata length      dates: ", len(dates)

  
  plt.plot_date(x=dates, y=readings_f, fmt="r-")
  plt.xticks(rotation=22)
  print "plottitle",dates[0], dates[-1]
  plt.title("Time vs Temp "+ get_config.config["serverLocation"] + "\nCovers "+
            dates[0].strftime("%Y-%m-%d %H:%M:%S ")+" to "+
            dates[-1].strftime("%Y-%m-%d %H:%M:%S"))
 
  plt.ylabel("Temp (F)")
  plt.grid(True)
  #plt.show()
  plt.savefig(outfilename)
  plt.close()


if __name__ == "__main__":
  import datetime
  outfilename = "plot_temp.png"
  dates = []
  readings_f = [] 

  for i in range(6):
    dates.append(datetime.datetime.today())
    readings_f.append(80+i*pow(-1,i))
    time.sleep( 2)
  plotdata(dates, readings_f, outfilename)
  print "made_data 1",readings_f
  readings_f= readings_f[0:0]
  dates = dates[0:0]

  print "clear data",readings_f
  for i in range(6):
      dates.append(datetime.datetime.today())
      readings_f.append(90+i*pow(-1,i))
      time.sleep( 2)
  print "made_data 2",readings_f
  plotdata(dates, readings_f, outfilename)
  print "after second plot",readings_f
  

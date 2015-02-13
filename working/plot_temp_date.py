import time
import numpy as np
import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.image as mpimg


def plotdata(dates, readings_f, filename):
  #days, temp_f = np.loadtxt("/home/pi/server_monitor/temps2015-01-01T10:09:44", unpack=True,
  #        converters={ 0: mdates.strpdate2num('%Y-%m-%dT%H:%M:%S')})

  print "in plotdata length readings_f: ", len(readings_f)
  print "in plotdata length      dates: ", len(dates)

  
  plt.plot_date(x=dates, y=readings_f, fmt="r-")
  plt.xticks(rotation=22)
  plt.title("Time vs Temp\nCovers "+
            dates[0].strftime("%Y-%m-%d %H:%M:%S ")+" to "+
            dates[-1].strftime("%Y-%m-%d %H:%M:%S"))
  plt.ylabel("Temp (F)")
  plt.grid(True)
  #plt.show()
  plt.savefig(filename)
  plt.close()


if __name__ == "__main__":
  import datetime
  filename = "plot_temp.png"
  dates = []
  readings_f = [] 

  for i in range(6):
    dates.append(datetime.datetime.today())
    readings_f.append(80+i*pow(-1,i))
    time.sleep( 2)
  plotdata(dates, readings_f, filename)
  print "made_data 1",readings_f
  readings_f= readings_f[0:0]
  dates = dates[0:0]

  print "clear data",readings_f
  for i in range(6):
      dates.append(datetime.datetime.today())
      readings_f.append(90+i*pow(-1,i))
      time.sleep( 2)
  print "made_data 2",readings_f
  plotdata(dates, readings_f, filename)
  print "after second plot",readings_f
  

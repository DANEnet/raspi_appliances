import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.image as mpimg

def plotdata(dates, readings, filename):
  #days, temp_f = np.loadtxt("/home/pi/server_monitor/temps2015-01-01T10:09:44", unpack=True,
  #        converters={ 0: mdates.strpdate2num('%Y-%m-%dT%H:%M:%S')})
  
  plt.plot_date(x=dates, y=readings, fmt="r-")
  plt.xticks(rotation=22)
  plt.title("Time vs Temp\nCovers "+
            dates[0].strftime("%Y-%m-%d %H:%M:%S ")+" to "+
            dates[-1].strftime("%Y-%m-%d %H:%M:%S"))
  plt.ylabel("Temp (F)")
  plt.grid(True)
  #plt.show()
  plt.savefig(filename)

def main():
  plotdata()

if __name__ == "__main__":
    main()

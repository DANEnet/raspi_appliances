import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.image as mpimg

plotdata():
  days, impressions = np.loadtxt("/home/pi/server_monitor/temps2015-01-01T10:09:44", unpack=True,
          converters={ 0: mdates.strpdate2num('%Y-%m-%dT%H:%M:%S')})

  plt.plot_date(x=days, y=impressions, fmt="r-")
  plt.title("Time vs Temp")
  plt.ylabel("Temp (F)")
  plt.grid(True)
  #plt.show()
  plt.savefig("out.png")

def main()
  plotdata()

if __name__ == "__main__":
    main()
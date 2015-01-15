import smbus
import time
import datetime

bus = smbus.SMBus(0)
#print dir(bus)
DEV_ADDR = 0x48
DEV_REG_MODE = 0
SAMP_PER_AVG = 6  # Number of samples in one measurement
SAMP_PERIOD=10.0  # PERIOD is seconds
                  # PERIOD * SAMPLES/Measurement = Interval between measurements 
last_valid = 0x12345

def c_to_f(in_temp):
  return (in_temp*1.8000) + 32
  

def get_temperature():
  global last_valid
  bus.write_byte_data(DEV_ADDR, 1, 0x60) # set up higher accuracy
  junk = bus.read_byte_data(DEV_ADDR, 0) # needed to keep thermomiter from going to 2 hex digits
  raw_temp = bus.read_word_data(DEV_ADDR, 0)
  hex_str = hex(raw_temp)
  print hex_str
  #if len(hex_str) == 5: #catch short reads
  #  last_valid = hex_str
  #else:
  #  hex_str = last_valid

  print  hex_str
    
  #t_c = int(hex_str[2], 16)/16.0 + int(hex_str[-2:], 16)
  t_c =  int(hex_str[-2:], 16)

  print raw_temp, hex(raw_temp), hex_str[-2:], t_c, c_to_f(t_c)
  last_valid = hex
  return c_to_f(t_c)

filename = "temps"+time.strftime("%Y-%m-%dT%H-%M-%S.tsv", time.localtime())
outfile = open(filename, "w")
while 1:
  t = 0.0
  for i in range(SAMP_PER_AVG):
    t += get_temperature()
    time.sleep(SAMP_PERIOD)
  timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
  average_temp = t/float(SAMP_PER_AVG)
  print timestamp, average_temp
  outfile.write("%s\t%3.1f\n"%(timestamp, average_temp))
  outfile.flush()





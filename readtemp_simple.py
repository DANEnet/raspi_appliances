import smbus
import time

bus = smbus.SMBus(0)
address = 0x68

def get_temperature():
  raw_temp = bus.read_byte_data(address, 1)
  return raw_temp

while 1:
  t = get_temperature()
  print t
  sleep 5
  

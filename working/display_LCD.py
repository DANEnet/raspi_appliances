import time
import  Adafruit_CharLCD as LCD

def display_LCD(time, tempc, tempf):
  try:
    lcd = LCD.Adafruit_CharLCDPlate()
  except:
    return
  lcd.set_color(1.0, 1.0, 1.0)
  lcd.clear()
  lcd.message('%5.1f F %5.1f C \n%s'%(tempf, tempc, time))



if __name__ == "__main__":
  time = "2017-03-11T22:32:46"
  tempc = 99.1
  tempf = 210.1
  display_LCD(time, tempc, tempf)

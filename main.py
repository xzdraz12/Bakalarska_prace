import json
from machine import Pin, UART
import Time, GPS, Files

#from ssd1306 import SSD1306_I2C

#import datetime
import requests
import utime
import time

#i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
#oled = SSD1306_I2C(128, 64, i2c)

gpsModule = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
print(gpsModule)

buff = bytearray(255)

TIMEOUT_GPS = False
FIX_STATUS_GPS = False

latitude = ""
longitude = ""
Observer_elevation = ""
satellites = ""
GPStime = ""
GPSdate = ""
MinElev = 20
DaysAhead = 2
SecondsPrediction = ""

AmateurSatellites = [25544, 51085, 42790] #ISS, VZLUSAT-2, VZLUSAT -1







def hi_name(name):

    {
        print ("ahoj"+name)
    }



while True:

    myname = "jakub"

    hi_name(myname)




















while True:

    #testTime()
    Time.ConvertToUnix()

    time.sleep(1)
    #getGPS(gpsModule)

    #if (FIX_STATUS_GPS == True):
        #print("Printing GPS data...")
        #print(" ")
        #print("Latitude: " + latitude)
        #print("Longitude: " + longitude)
        #print("Satellites: " + satellites)
        #print("Time: " + GPStime)
        #print("----------------------")

        #FIX_STATUS_GPS = False

    #if (TIMEOUT_GPS == True):
        #print("No GPS data is found.")
        #TIMEOUT_GPS = False
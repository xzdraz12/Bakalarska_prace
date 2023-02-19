
import utime
import settings
from GPS import GPS
#from waiting import wait

def welcome():

    settings.lcd.putstr("Welcome")
    utime.sleep(2)
    settings.lcd.clear()
    settings.lcd.putstr("Version 2023")
    utime.sleep(2)
    settings.lcd.clear()

def GettingGPS():

    #wait(lambda : GPS.GPSisReady(), waiting_for="Waiting for GPS signal")
    settings.lcd.clear()
    settings.lcd.putstr("Waiting for GPS haha")
    settings.lcd.blink_cursor_on()
    while GPS.GPSisReady == True: #or settings.button.value()==1:
        settings.lcd.putstr("GPS obtained")
        utime.sleep(1.5)
        continue


def SetWifi():

    print("kk")

def ScrollMenu():

    settings.lcd.clear()
    settings.lcd.putstr("WiFi")




        







import machine

import GPS
import menu
import wifi
import utime
from machine import Pin

machine.freq(240000000)

#uvitani
menu.Welcome()

#pripojeni k WiFi
wifi.ConnectWifi()

#ziskani aktualniho casu
ntptime.settime()
print("UTC time: "+str(utime.localtime()[0]))
print("time from NTP server")

#ziskani dat GPS
GPS.OperateGPS(GPS.gpsModule)

#menu







import machine

import Compass
import GPS
import Satellites
import menu
import settings
import wifi
import utime

from settings import oled as oled


machine.freq(240000000)

#uvitani
menu.Welcome()

#pripojeni k WiFi
wifi.ConnectWifi()

#ziskani aktualniho casu
menu.SetNTP()

oled.fill(0)
oled.show()
oled.text("NTP time",0,0)
oled.text("obtained",0,10)
oled.show()
utime.sleep(2)

print("UTC time: "+str(utime.localtime()))
print("time from NTP server")

#ziskani dat GPS
GPS.GPSStatus()
GPS.OperateGPS(GPS.gpsModule)
GPS.GPSStatus()

#ziskani dat o deklinaci a inklinaci
Compass.GetCompassApi()

#kalibrace kompasu


#satelity
Satellites.DownloadAPI()
Satellites.DownloadForDesiredPass_loop()

#menu







import machine
import urequests

from Compass import  HMC5883L
import CompassCalibration
import Satellites
import menu
import settings
import wifi
from GPS import RawGPS
import GPS
import utime
import ntptime

#
#
# menu.Welcome()
# GPS.GPSStatus()
# GPS.OperateGPS(GPS.gpsModule)
# GPS.GPSStatus()
# utime.sleep(3)
# settings.lcd.clear()
# GPS.GPS_info()
#
#
machine.freq(240000000)
# menu.Welcome()
# wifi.ConnectWifi()
# ntptime.settime()
#
# settings.lcd.clear()
# #settings.lcd.putstr("UTC time: "+str(utime.localtime()[0])+)
# #print(RawGPS().GPSaltitude)
# # GPS.GPSStatus()
# # GPS.OperateGPS(GPS.gpsModule)
# # GPS.GPSStatus()
# #
# # GPS.GPS_info()
# Satellites.DownloadAPI()
# while True:
#
#
#     Satellites.DownloadForDesiredPass_loop()

CompassCalibration.GetCompassApi()
CompassCalibration.Calibrate()
sensor = HMC5883L()

while True:
    utime.sleep(1)
    x, y, z = sensor.read()
    print(sensor.format_result(x, y, z))



















#print("1")
#two = _thread.start_new_thread(wifi.ConnectWifi, ())

#print(wifi.wlan.isconnected())
#utime.sleep(2)


#wifi.ConnectWifi()

#print(wifi.wlan.isconnected())


# menu.menuTest()

#menu.Welcome()



#Compass.Calibration()



# while True:
#     #sleep(1)
#     x, y, z = Compass.read()
#     print(Compass.format_result(x, y, z))

# wifi.ConnectWifi()
# settings.GetNTPtime()

#Satellites.DownloadAPI()

# if wifi.wlan.isconnected():
#     req = urequests.get("https://example.com")
#     print(req.status_code)
#     print(type(req))




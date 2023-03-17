import urequests
import Satellites
import menu
import settings
import wifi
from GPS import RawGPS
import GPS
import utime

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


menu.Welcome()

wifi.ConnectWifi()
settings.Get_Local_NTP_time()

settings.lcd.clear()
#settings.lcd.putstr("UTC time: "+str(utime.localtime()[0])+)
#print(RawGPS().GPSaltitude)
GPS.GPSStatus()
GPS.OperateGPS(GPS.gpsModule)
GPS.GPSStatus()

GPS.GPS_info()

while True:

    Satellites.DownloadAPI()
    Satellites.DownloadForDesiredPass()



















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




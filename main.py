import urequests

#import Satellites
import settings
import wifi
#
# menu.Welcome()
# GPS.GPSStatus()
# GPS.OperateGPS(GPS.gpsModule)
# GPS.GPSStatus()
# utime.sleep(3)
# settings.lcd.clear()
# GPS.GPS_info()
#print("1")
#two = _thread.start_new_thread(wifi.ConnectWifi, ())

#print(wifi.wlan.isconnected())
#utime.sleep(2)


#wifi.ConnectWifi()

#print(wifi.wlan.isconnected())


# menu.menuTest()

#menu.Welcome()



#Compass.Calibration()

#Satellites.DownloadAPI()

# while True:
#     #sleep(1)
#     x, y, z = Compass.read()
#     print(Compass.format_result(x, y, z))

wifi.ConnectWifi()
settings.GetNTPtime()

if wifi.wlan.isconnected():
    req = urequests.get("https://example.com")
    print(req.status_code)
    print(req.text)





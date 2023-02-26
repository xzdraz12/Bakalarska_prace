import machine
import utime
import network
import menu
import settings
import GPS
import _thread

import wifi
# menu.Welcome()
# GPS.GPSStatus()
# GPS.OperateGPS(GPS.gpsModule)
# GPS.GPSStatus()
# utime.sleep(3)
# settings.lcd.clear()
# GPS.GPS_info()

#print("1")
#two = _thread.start_new_thread(wifi.ConnectWifi, ())

# print(wifi.wlan.isconnected())
# utime.sleep(2)
#wifi.wlan.connect(wifi.ssid, wifi.password)


#wifi.ConnectWifi()

#print(wifi.wlan.isconnected())




while True:
    menu.menuTest()
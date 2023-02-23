import machine
import utime

import menu
import settings
import GPS
import _thread



menu.Welcome()
menu.GPSStatus()
#two = _thread.start_new_thread(GPS.OperateGPS(GPS.gpsModule), ())
GPS.OperateGPS(GPS.gpsModule)
menu.GPSStatus()
utime.sleep(3)
settings.lcd.clear()
GPS.GPS_info()


while True:
    menu.menuTest()
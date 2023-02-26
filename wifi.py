import network
from time import sleep

import utime

import settings
import wifi

global ssid, password, CONNECTED_STATUS
ssid = "Musli"
password = "vodak2019"
CONNECTED_STATUS = False

wlan = network.WLAN(network.STA_IF)

def ConnectWifi():

    #wlan.active(False)

    while True:

        if wlan.isconnected() == False or wlan.status() == "STAT_IDLE" or wlan.status() == "STAT_CONNECT_FAIL":
            settings.lcd.clear()
            settings.lcd.putstr("WiFi Disconnected")
            while wlan.isconnected() == False or wlan.status() == "STAT_IDLE" or wlan.status() == "STAT_CONNECT_FAIL":
                wlan.active(True)
                wlan.connect(ssid, password)
                print("snazim se spojit")
                utime.sleep(3)
            utime.sleep(3)

        elif wlan.status() == "STAT_GOT_IP":
            settings.lcd.clear()
            settings.lcd.putstr("WiFi Connected" + ssid)
            utime.sleep(3)
            settings.lcd.clear()
            break








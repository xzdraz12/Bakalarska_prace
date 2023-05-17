import network
import utime
import settings
import sys
from settings import oled as oled

global ssid, password
ssid = "Musli"
password = "vodak2019"

global wlan
wlan = network.WLAN(network.STA_IF)

def ConnectWifi():
    wlan.active(False)
    utime.sleep(.5)
    wlan.active(True)
    attempts = 0

    oled.fill(0)
    oled.show()
    oled.text("Connecting to",0,0)
    oled.text("WiFi", 0,10)
    oled.show()
    print("Connecting to WiFi")

    while not wlan.isconnected():
        wlan.connect(ssid, password)
        utime.sleep(5)
        attempts = attempts +1
        if attempts == 5:
            oled.fill(0)
            oled.show()
            oled.text("Time Out",0,0)
            print("Time Out")
            break
        if wlan.isconnected():
            break

    if wlan.isconnected():
        oled.fill(0)
        oled.show()
        oled.text("WiFi is", 0,0)
        oled.text("connected",0,10)
        oled.show()
        print("Connected")
        utime.sleep(2)
        oled.fill(0)
        oled.show()
    else:
        print("Error, please restart the device")
        oled.fill(0)
        oled.show()
        oled.text("Error, please",0,0)
        oled.text("restart the device", 0,10)
        oled.text("by unplugging", 0,20)
        oled.show()


def wifiStatus():
    info = wlan.ifconfig()
    oled.fill(0)
    oled.show()
    oled.text("IP:",0,0)
    oled.text(info[0],0,10)
    oled.text("Mask:",0,20)
    oled.text(info[1],0,30)
    oled.text("Gtw:",0,40)
    oled.text(info[2],0,50)
    #oled.text("DNS:"+info[3],0,30)
    oled.show()

ConnectWifi()
wifiStatus()
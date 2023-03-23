import network
import utime
import settings
import sys
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

    print("Connecting to wifi")
    settings.lcd.clear()
    settings.lcd.putstr("Connecting to WiFi")
    settings.lcd.blink_cursor_on()

    while not wlan.isconnected():
        wlan.connect(ssid, password)
        utime.sleep(5)
        attempts = attempts +1
        if attempts == 5:
            settings.lcd.clear()
            settings.lcd.putstr("Time Out")
            break
        if wlan.isconnected():
            break

    if wlan.isconnected():
        settings.lcd.clear()
        print("Connected")
        settings.lcd.blink_cursor_off()
        settings.lcd.clear()
        settings.lcd.putstr("WiFi is connected")
        utime.sleep(2)
        settings.lcd.clear()

    else:
        print("Error, please restart the device")
        settings.lcd.clear()
        settings.lcd.putstr("Error, please restart the device")

        for i in range (1, 10):
            settings.lcd.clear()
            settings.lcd.putstr(i)
        sys.exit()



#ConnectWifi()

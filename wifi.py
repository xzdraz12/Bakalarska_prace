import network
import utime
import settings

global ssid, password
ssid = "Musli"
password = "vodak2019"


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

    # #wlan.active(False)
    #
    # while True:
    #
    #     if wlan.isconnected() == False or wlan.status() == "STAT_IDLE" or wlan.status() == "STAT_CONNECT_FAIL":
    #         settings.lcd.clear()
    #         settings.lcd.putstr("WiFi Disconnected")
    #         while wlan.isconnected() == False or wlan.status() == "STAT_IDLE" or wlan.status() == "STAT_CONNECT_FAIL":
    #             wlan.active(True)
    #             wlan.connect(ssid, password)
    #             print("snazim se spojit")
    #             utime.sleep(3)
    #         utime.sleep(3)
    #
    #     elif wlan.status() == "STAT_GOT_IP":
    #         settings.lcd.clear()
    #         settings.lcd.putstr("WiFi Connected" + ssid)
    #         utime.sleep(3)
    #         settings.lcd.clear()
    #         break

import network
import machine
from time import sleep


ssid = "Musli"
password = "vodak2019"

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected()== False:
        print("Připojování")

        sleep(1)

    ip = wlan.ifconfig()[0]
    print("ip je: "+ ip)


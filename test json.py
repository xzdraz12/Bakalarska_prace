import network  # import network library to work with Wi-Fi
import time  # import time library
from machine import Pin  # import only Pin library from machine module
import urequests
import ujson
import utime

# Wi-Fi connected status LED
# define and set default state
LED = Pin(16, Pin.OUT)
LED.value(0)

# Set Wi-Fi network to Station Interface
wlan = network.WLAN(network.STA_IF)
wlan.active(True)  # enable Wi-Fi interface

# print Wi-Fi Scan of APs around
aps_scan = wlan.scan()  # store last Wi-Fi AP scan
countAPs = len(aps_scan)  # get number of APs found
for i in range(countAPs):  # iterate over whole scan one-by-one
    print(aps_scan[i])  # print information about AP

# connect to predefined AP wlan.connect(SSID, Password)
# wlan.connect("LPWAN-IoT-XY", "LPWAN-IoT-XY-WiFi") # replace XY with your station number (correct 1 up to 10)
# wlan.connect("LPWAN-IoT-00", "LPWAN-IoT-00-WiFi") # example for teacher station with number 00
wlan.connect("xRD-03E9A5D5CA", "y5FrJ3?K6cFVM_tr")

# while Wi-Fi is not connected
while not wlan.isconnected():
    print("WIFI STATUS CONNECTED: " + str(
        wlan.isconnected()))  # print current status aka False=Not connect, True=Connected

    time.sleep_ms(500)  # check period set to 500 ms

LED.value(1)  # set Wi-Fi status LED to High/On

# after connection to Wi-Fi print current Wi-Fi configuration
print(wlan.ifconfig())


def test():
    global ListOfPositions

    seconds = "40"  # zde lze menit velikost, 40 sekund zvlada, napr 50 uz ne
    url = "https://api.n2yo.com/rest/v1/satellite/positions/39469/49.3125/17.3750/0/" + seconds + "/&apiKey=TLX2JG-94DFXJ-K57JEF-4XB1"
    # url = "https://api.n2yo.com/rest/v1/satellite/positions/" + "39469" + "/" + latitude + "/" + longitude + "/" + ObserverAltitude + "/" + seconds + "/&apiKey=" + licenseKey

    try:
        GetPositions = urequests.get(url).json()
    except Exception as e:
        print("ERROR: " + str(e))
        return
    print(GetPositions['info'])
    # print(GetPositions['positions'])
    # GetPositions_json = ujson.loads(GetPositions)

    ListOfPositions = []

    for jsonValue in GetPositions['positions']:
        print(jsonValue)

        timestamp = int(jsonValue["timestamp"])
        print(time.localtime(timestamp))
        timestamp = timestamp + (3600 * 2)
        azimuth = float(jsonValue["azimuth"])
        elevation = float(jsonValue["elevation"])

        PositionTuple = (timestamp, azimuth, elevation)
        ListOfPositions.append(PositionTuple)

    for i in range(40):
        # print(ListOfPositions[i])
        CurAzimuth = str(ListOfPositions[i][1])
        CurElev = str(ListOfPositions[i][2])

    """
    hilfelist = []

    for i in range(0, 30):  # list naplnim
        hilfelist.append(i)

    for x in hilfelist:
        timestamp = int(ujson.dumps(GetPositions_json["positions"][x]["timestamp"]))
        timestamp = timestamp + (3600 * 2)
        azimuth = float(ujson.dumps(GetPositions_json["positions"][x]["azimuth"]))
        elevation = float(ujson.dumps(GetPositions_json["positions"][x]["elevation"]))

        PositionTuple = (timestamp, azimuth, elevation)
        ListOfPositions.append(PositionTuple)

    while True:
        if utime.time() == ListOfPositions[1][0]:

            for i in hilfelist:
                print(ListOfPositions[i][2])
                #settings.lcd.clear()
                CurAzimuth = str(ListOfPositions[i][1])
                CurElev = str(ListOfPositions[i][2])
                #settings.lcd.putstr("az: " + CurAzimuth + "        el: " + CurElev)

                utime.sleep(1)

            break
        break

    """


test()

print("End of script")
# end of script
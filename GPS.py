from machine import UART
import utime, time

import settings
from settings import oled as oled

gpsModule = UART(0, baudrate=9600)
buff = bytearray(255)

TIMEOUT = False
FIX_STATUS_GPS = True

latitude = "49.1337"
longitude = "16.3429"
satellites = "manually set"
GPStime = ""
altitude = "280"


def RawGPS(gpsModule):
    global FIX_STATUS_GPS, TIMEOUT, latitude, longitude, satellites, GPStime, GPSaltitude,altitude

    timeout = time.time() + 8
    while True:
        gpsModule.readline()
        buff = str(gpsModule.readline())
        parts = buff.split(',')
        print(buff)
        if (parts[0] == "b'$GNGGA" and len(parts) == 15): #spíš GNGGA
            if (parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6] and parts[7]):
                print(buff)
                latitude = convertToDegree(parts[2])
                if (parts[3] == 'S'):
                    latitude = -latitude
                longitude = convertToDegree(parts[4])
                if (parts[5] == 'W'):
                    longitude = -longitude
                satellites = parts[7]
                altitude = parts[9]
                FIX_STATUS_GPS = True
                break

        if (time.time() > timeout):
            TIMEOUT = True
            break
        utime.sleep_ms(500)

       # if (TIMEOUT == True):
        #    TIMEOUT == False

def convertToDegree(RawDegrees):
    RawAsFloat = float(RawDegrees)
    firstdigits = int(RawAsFloat / 100)
    nexttwodigits = RawAsFloat - float(firstdigits * 100)

    Converted = float(firstdigits + nexttwodigits / 60.0)
    Converted = '{0:.6f}'.format(Converted)
    return str(Converted)


def OperateGPS(gpsModule):
    while True:
        RawGPS(gpsModule)
        if (FIX_STATUS_GPS == True):
            break

def GPSStatus():
    if FIX_STATUS_GPS == False:
        oled.fill(0)
        oled.show()
        oled.text("Waiting for GPS", 0,0)
        oled.show()
        print("Waiting for GPS ")

    elif FIX_STATUS_GPS == True:
        oled.fill(0)
        oled.show()
        oled.text("GPS obtained",0,0)
        oled.show()
        print("GPS obtained")
        utime.sleep(3)

def GPS_info():

    while settings.BTN_ENC.value()==0:
        continue

    oled.fill(0)
    oled.show()
    oled.text("Lat:"+latitude,0,0)
    oled.text("Lon:"+longitude,0,10)
    oled.text("Alt:"+altitude,0,20)
    oled.text("Sat:"+satellites,0,30)
    oled.show()

    print("Lat: "+latitude)
    print("Lon: "+longitude)
    print("Time: "+GPStime)
    print("Altitude: "+altitude)
    print("Satellites: "+satellites)

    while settings.BTN_ENC.value()==1:
        continue

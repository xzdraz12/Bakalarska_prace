
from machine import Pin, UART
import utime, time
import settings


gpsModule = UART(0, baudrate=9600, tx=Pin(12), rx=Pin(13))

buff = bytearray(255)

TIMEOUT = False

FIX_STATUS_GPS = False

latitude = ""
longitude = ""
satellites = ""
GPStime = ""


def RawGPS(gpsModule):
    global FIX_STATUS_GPS, TIMEOUT, latitude, longitude, satellites, GPStime

    timeout = time.time() + 8
    while True:
        #main.baton.acquire()
        gpsModule.readline()
        buff = str(gpsModule.readline())
        parts = buff.split(',')

        if (parts[0] == "b'$GPGGA" and len(parts) == 15):
            if (parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6] and parts[7]):
                #print(buff)

                latitude = convertToDegree(parts[2])
                if (parts[3] == 'S'):
                    latitude = -latitude
                longitude = convertToDegree(parts[4])
                if (parts[5] == 'W'):
                    longitude = -longitude
                satellites = parts[7]
                GPStime = parts[1][0:2] + ":" + parts[1][2:4] + ":" + parts[1][4:6]
                FIX_STATUS_GPS = True
                break

        if (time.time() > timeout):
            TIMEOUT = True
            break
        utime.sleep_ms(500)

        if (TIMEOUT == True):
            TIMEOUT == False

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
            #_thread.exit()
            break



def GPS_info():
    settings.lcd.putstr("zemepisna sirka:")
    settings.lcd.putstr(latitude)
    utime.sleep(3)

    settings.lcd.clear()

    settings.lcd.putstr("zem. delka:      ")
    settings.lcd.putstr(longitude)
    utime.sleep(3)

    settings.lcd.clear()

    settings.lcd.putstr("UTC cas:        ")
    settings.lcd.putstr(GPStime)

    utime.sleep(3)

    settings.lcd.clear()

    settings.lcd.putstr("Pocet satelitu: ")
    settings.lcd.putstr(satellites)
    utime.sleep(3)
    settings.lcd.clear()

    print(longitude)
    print(GPStime)
    print(satellites)
# import utime, time
# #global FIX_STATUS_GPS
# #FIX_STATUS_GPS = True
# from machine import UART, Pin
#
# global FIX_STATUS_GPS, TIMEOUT, latitude, longitude, satellites, GPStime
# latitude = ""
# longitude = ""
# satellites = ""
# GPStime = ""
# TIMEOUT = False
# FIX_STATUS_GPS = False
#
# gpsModule = UART(0, baudrate=9600, tx=Pin(12), rx=Pin(13))
# def getGPS(gpsModule):
#     global FIX_STATUS_GPS
#     while True:
#
#
#         # print(gpsModule)
#
#         buff = bytearray(255)
#
#         timeout = time.time() + 8
#         while True:
#             gpsModule.readline()
#             buff = str(gpsModule.readline())
#             parts = buff.split(',')
#             print("tutaj")
#             if (parts[0] == "b'$GPGGA" and len(parts) == 15):
#                 if (parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6] and parts[7]):
#                     print(buff)
#                     print("a co tady")
#                     latitude = convertToDegree(parts[2])
#                     if (parts[3] == 'S'):
#                         latitude = -latitude
#                     longitude = convertToDegree(parts[4])
#                     if (parts[5] == 'W'):
#                         longitude = -longitude
#                     satellites = parts[7]
#                     GPStime = parts[1][0:2] + ":" + parts[1][2:4] + ":" + parts[1][4:6]
#                     FIX_STATUS_GPS = True
#                     break
#
#             if (time.time() > timeout):
#                 TIMEOUT = True
#                 break
#             print("achoj")
#             utime.sleep_ms(500)
#         while FIX_STATUS_GPS == True:
#             break
#
#
#
# def convertToDegree(RawDegrees):
#     RawAsFloat = float(RawDegrees)
#     firstdigits = int(RawAsFloat / 100)
#     nexttwodigits = RawAsFloat - float(firstdigits * 100)
#
#     Converted = float(firstdigits + nexttwodigits / 60.0)
#     Converted = '{0:.6f}'.format(Converted)
#     return str(Converted)
#




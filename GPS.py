
from machine import Pin, UART
import utime, time
import settings


gpsModule = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

buff = bytearray(255)

TIMEOUT = False

FIX_STATUS_GPS = False

latitude = ""
longitude = ""
satellites = ""
GPStime = ""


def RawGPS(gpsModule):
    global FIX_STATUS_GPS, TIMEOUT, latitude, longitude, satellites, GPStime, GPSaltitude

    timeout = time.time() + 8
    while True:
        #main.baton.acquire()
        gpsModule.readline()
        buff = str(gpsModule.readline())
        parts = buff.split(',')
        print(buff)
        if (parts[0] == "b'$GPGGA" and len(parts) == 15):
            if (parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6] and parts[7]):
                print(buff)
                print("achoj")
                latitude = convertToDegree(parts[2])
                if (parts[3] == 'S'):
                    latitude = -latitude
                longitude = convertToDegree(parts[4])
                if (parts[5] == 'W'):
                    longitude = -longitude
                satellites = parts[7]
                GPStime = parts[1][0:2] + ":" + parts[1][2:4] + ":" + parts[1][4:6]
                #GPSaltitude = parts[9]
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

def GPSStatus():
    if FIX_STATUS_GPS == False:
        # while GPS.FIX_STATUS_GPS == False:

        settings.lcd.clear()
        settings.lcd.putstr("Waiting for GPS ")
        print("Waiting for GPS ")
        settings.lcd.blink_cursor_on()
        #utime.sleep(.5)
        #break
        # while GPS.FIX_STATUS_GPS == False:
        # continue

    # elif GPS.FIX_STATUS_GPS == True:
    elif FIX_STATUS_GPS == True:
        settings.lcd.clear()
        settings.lcd.blink_cursor_off()
        settings.lcd.putstr("GPS obtained")
        print("GPS obtained ")
        utime.sleep(3)

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

#OperateGPS(gpsModule)
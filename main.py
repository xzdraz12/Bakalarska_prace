#import calendar
import utime
from machine import Pin, UART
#from ssd1306 import SSD1306_I2C

#import utime
import time

#i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
#oled = SSD1306_I2C(128, 64, i2c)

gpsModule = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
print(gpsModule)

buff = bytearray(255)

TIMEOUT_GPS = False
FIX_STATUS_GPS = False

latitude = ""
longitude = ""
satellites = ""
GPStime = ""
GPSdate = ""

def ConvertToUTC(EpochTime):

    UTCTime = utime.gmtime(EpochTime)
    return UTCTime

def SetTime():
    RaWTime = GPStime.split(':')

    rtc.hour = GPStime[0]
    rtc.minute = GPStime[1]
    rtc.second = GPStime[2]

    RaWDate = GPSdate.split('.')

    rtc.day = RaWDate[0]
    rtc.month = RaWDate[1]
    rtc.year = RaWDate[2]


def testTime():
    print(utime.gmtime(0))


    #print(time.localtime())


def ConvertToUnix():
    CurrentTime = "15:33:00"
    RawCurrentTime = CurrentTime.split(':')
    Hour = RawCurrentTime[0]
    Minute = RawCurrentTime[1]
    Second = RawCurrentTime[2]

    Year = 2022
    Day = 15
    Month = 10




    #RawDate = GPSDate.split('.')
    #Day = RawDate[0]
    #Month = RawDate[1]
    #Year = RawDate[2]


    #EpochTime = calendar.timegm()

    #print ("time since epoch: "+EpochTime)


    #dateAndTime = datetime(Year, Month, Day, Hour, Minute, Second)
    #UnixTimestamp = int(dateAndTime.timestamp())
    #return UnixTimestamp




def getGPS(gpsModule):
    global FIX_STATUS_GPS, FIX_STATUS_DATE, TIMEOUT_GPS, latitude, longitude, satellites, GPStime, GPSdate


    timeout = time.time() + 8
    while True:
        gpsModule.readline()
        buff_gps = str(gpsModule.readline())
        parts_gps = buff_gps.split(',')
        parts_date = buff_gps.split(',')

        if (parts_gps[0] == "b'$GPGGA" and len(parts_gps) == 15):
            if (parts_gps[1] and parts_gps[2] and parts_gps[3] and parts_gps[4] and parts_gps[5] and parts_gps[6] and parts_gps[7]):
                #print(buff_gps)

                latitude = convertToDegree(parts_gps[2])
                if (parts_gps[3] == 'S'):
                    latitude = -latitude
                longitude = convertToDegree(parts_gps[4])
                if (parts_gps[5] == 'W'):
                    longitude = -longitude
                satellites = parts_gps[7]
                GPStime = parts_gps[1][0:2] + ":" + parts_gps[1][2:4] + ":" + parts_gps[1][4:6]


                FIX_STATUS_GPS = True
                break

        if (parts_gps[0] == "b'$GPRMC" and len(parts_gps) == 13):
            if (parts_gps[1] and parts_gps[2] and parts_gps[3] and parts_gps[4] and parts_gps[5] and parts_gps[6] and parts_gps[7]):

                GPSdate = parts_date[1][0:2] + "." + parts_date[1][2:4] + "." + parts_date[1][4:6]+"." #DDMMYY

                FIX_STATUS_DATE = True
                break




        if (time.time() > timeout):
            TIMEOUT_GPS = True
            break
        time.sleep_ms(500)


def convertToDegree(RawDegrees):
    RawAsFloat = float(RawDegrees)
    firstdigits = int(RawAsFloat / 100)
    nexttwodigits = RawAsFloat - float(firstdigits * 100)

    Converted = float(firstdigits + nexttwodigits / 60.0)
    Converted = '{0:.6f}'.format(Converted)
    return str(Converted)


while True:

    testTime()
    time.sleep(1)
    #getGPS(gpsModule)

    #if (FIX_STATUS_GPS == True):
        #print("Printing GPS data...")
        #print(" ")
        #print("Latitude: " + latitude)
        #print("Longitude: " + longitude)
        #print("Satellites: " + satellites)
        #print("Time: " + GPStime)
        #print("----------------------")

        #FIX_STATUS_GPS = False

    #if (TIMEOUT_GPS == True):
        #print("No GPS data is found.")
        #TIMEOUT_GPS = False
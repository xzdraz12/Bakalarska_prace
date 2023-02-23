from machine import Pin, UART
import Time

#from ssd1306 import SSD1306_I2C

#import datetime
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
Observer_elevation = ""
satellites = ""
GPStime = ""
GPSdate = ""
MinElev = 20
DaysAhead = 2
SecondsPrediction = ""

AmateurSatellites = [25544, 51085, 42790] #ISS, VZLUSAT-2, VZLUSAT -1







def hi_name(name):

    {
        print ("ahoj"+name)
    }



#while True:

    myname = "jakub"

    hi_name(myname)




















while True:

    #testTime()
    Time.ConvertToUnix()

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

    gpsModule = UART(0, baudrate=9600, tx=Pin(12), rx=Pin(13))


    def getGPS(gpsModule):
        global FIX_STATUS_GPS, TIMEOUT_GPS, latitude, longitude, satellites
        buff = bytearray(255)
        FIX_STATUS_GPS = False
        TIMEOUT_GPS = False
        timeout = time.time() + 8
        print("hehe")
        while True:
            gpsModule.readline()
            buff_gps = str(gpsModule.readline())
            parts_gps = buff_gps.split(',')
            print(buff_gps)
            # parts_date = buff_gps.split(',')
            print("tady")
            if (parts_gps[0] == "b'$GPGGA" and len(parts_gps) == 15):
                if (parts_gps[1] and parts_gps[2] and parts_gps[3] and parts_gps[4] and parts_gps[5] and parts_gps[
                    6] and parts_gps[7]):
                    print(buff_gps)
                    print("a co tady)")
                    latitude = convertToDegree(parts_gps[2])
                    if (parts_gps[3] == 'S'):
                        latitude = -latitude
                    longitude = convertToDegree(parts_gps[4])
                    if (parts_gps[5] == 'W'):
                        longitude = -longitude
                    FIX_STATUS_GPS = True
                    break

            if (time.time() > timeout):
                TIMEOUT_GPS = True
                break
            time.sleep_ms(500)
            print("tutaj")
            while FIX_STATUS_GPS == True:
                continue



















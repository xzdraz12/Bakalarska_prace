from machine import UART, Pin
import time





def getGPS(gpsModule):
    global FIX_STATUS_GPS, FIX_STATUS_DATE, TIMEOUT_GPS, latitude, longitude, satellites, GPStime, GPSdate
    FIX_STATUS_GPS = False
    timeout = time.time() + 8
    while True:
        gpsModule.readline()
        buff_gps = str(gpsModule.readline())
        parts_gps = buff_gps.split(',')
        parts_date = buff_gps.split(',')

        if (parts_gps[0] == "b'$GPGGA" and len(parts_gps) == 15):
            if (parts_gps[1] and parts_gps[2] and parts_gps[3] and parts_gps[4] and parts_gps[5] and parts_gps[
                6] and parts_gps[7]):
                # print(buff_gps)

                latitude = GPS.convertToDegree(parts_gps[2])
                if (parts_gps[3] == 'S'):
                    latitude = -latitude
                longitude = GPS.convertToDegree(parts_gps[4])
                if (parts_gps[5] == 'W'):
                    longitude = -longitude
                satellites = parts_gps[7]
                GPStime = parts_gps[1][0:2] + ":" + parts_gps[1][2:4] + ":" + parts_gps[1][4:6]

                # FIX_STATUS_GPS = True
                break

        if (parts_gps[0] == "b'$GPRMC" and len(parts_gps) == 13):
            if (parts_gps[1] and parts_gps[2] and parts_gps[3] and parts_gps[4] and parts_gps[5] and parts_gps[
                6] and parts_gps[7]):
                GPSdate = parts_date[1][0:2] + "." + parts_date[1][2:4] + "." + parts_date[1][4:6] + "."  # DDMMYY

                # FIX_STATUS_DATE = True
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


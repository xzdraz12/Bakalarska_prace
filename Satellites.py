import ujson
import utime
import math
import urequests
import GPS
import Motors
import settings


# licenseKey = "TLX2JG-94DFXJ-K57JEF-4XB1"
# MinElevation = "0"
# DaysPrediction = "2"
# ObserverAltitude = "0"
# latitude = "49.3125"
# longitude = "17.3750"

licenseKey = settings.licenseKey
MinElevation = settings.MinElevation
DaysPrediction = settings.DaysPrediction
ObserverAltitude = settings.ObserverAltitude
latitude = GPS.latitude
longitude = GPS.longitude


RadioSatellites =["14781", "53385","43678","53385","25544","51085", "49396"]

def DownloadAPI():
    #stahuju data, kdy nastane dalsi prelet
    global Pass_start, Pass_end, Satname, Pass_azimuth
    Pass_start = {}
    Pass_end = {}
    Pass_azimuth = {}
    Satname = {}

    settings.lcd.clear()
    settings.lcd.putstr("Downloading satellite data")
    settings.lcd.blink_cursor_on()

    for satID in RadioSatellites:
        url = "https://api.n2yo.com/rest/v1/satellite/radiopasses/" + satID + "/" + latitude + "/" + longitude + "/" + ObserverAltitude + "/" + DaysPrediction + "/" + MinElevation + "/&apiKey=" + licenseKey
        print(url)

        GetPasses = urequests.get(url)

        GetPasses_json = GetPasses.json()

        SatName = ujson.dumps(GetPasses_json["info"]["satname"])

        for JsonValue in GetPasses_json['passes']:

            StartUTC = ujson.dumps(JsonValue["startUTC"])
            EndUTC = ujson.dumps(JsonValue["endUTC"])
            StartAzimuth = ujson.dumps(JsonValue["startAz"])

            JsonValue = str(JsonValue)
            nickname = satID+"_"+JsonValue

            Pass_start[nickname]= int(StartUTC)
            Pass_end[nickname] = int(EndUTC)
            Pass_azimuth[nickname]=float(StartAzimuth)
            Satname[nickname] = str(SatName)
            


    Sorted_Pass_start = sorted(Pass_start.items(), key=lambda x:x[1])
    Pass_start = Sorted_Pass_start

def DownloadForDesiredPass():
    global CurrentSatId, CurrentSatName

    RawID = Pass_start[0][0]
    parts = RawID.split("_")
    CurrentSatId = parts[0]
    CurrentSatName = str(Satname[RawID])

    UNIX_start = Pass_start[0][1]
    UNIX_end = Pass_end[RawID]

    StartAZ = Pass_azimuth[RawID]

    print(StartAZ)

    Begin = int(UNIX_start)
    Begin = Begin + (settings.DaylightSaving + settings.timezone) *3600

    End = int(UNIX_end)
    End = End + (settings.DaylightSaving + settings.timezone) *3600


    PassDuration = End - Begin

    PassDuration = str(PassDuration)

    SlewOnlyOnce = True
    while True:
        CurrentTimeInMyTimezone = utime.time() + (settings.DaylightSaving + settings.timezone) * 3600

        TimeToPass = Begin - CurrentTimeInMyTimezone
        Hours_float = TimeToPass / 3600
        Minutes, Hours = math.modf(Hours_float)
        Hours = str(int(Hours))
        Minutes_OK = (60 * Minutes)
        Seconds = Minutes_OK % 1
        Minutes_OK = str(int(Minutes_OK))
        Seconds_OK = str(int(60 * Seconds))

        print(TimeToPass)

        if CurrentTimeInMyTimezone > End:
            print("Bad Timezone")
            print("use settings to adjust timezone")

            settings.lcd.clear()
            settings.lcd.putstr("Bad timezone")
            utime.sleep(1)
            settings.lcd.clear()
            settings.lcd.putstr("use settings to adjust the timezone")
            break


        settings.lcd.clear()
        settings.lcd.putstr(CurrentSatId+"in:     ")
        settings.lcd.putstr(Hours + ":" + Minutes_OK + ":" + Seconds_OK)
        utime.sleep(1)

        if SlewOnlyOnce == True and TimeToPass <=50:
            settings.lcd.clear()
            settings.lcd.putstr("Slewing into start position")

            Motors.rotate_azimuth_change_speed(StartAZ, "cw", 8)
            
            settings.lcd.clear()

            SlewOnlyOnce = False

        if TimeToPass <= 5:
            while True:
                url = "https://api.n2yo.com/rest/v1/satellite/positions/" + CurrentSatId + "/" + latitude + "/" + longitude + "/" + ObserverAltitude + "/" + "35" + "/&apiKey=" + licenseKey
                GetPositions = urequests.get(url)
                GetPositions_json = GetPositions.json()

                global ListOfPositions
                ListOfPositions = []

                for JsonValue in GetPositions_json['positions']:
                    timestamp = int(ujson.dumps(JsonValue["timestamp"]))
                    timestamp = timestamp + (3600 * settings.timezone)
                    azimuth = float(ujson.dumps(JsonValue["azimuth"]))
                    elevation = float(ujson.dumps(JsonValue["elevation"]))

                    PositionTuple = (timestamp, azimuth, elevation)
                    ListOfPositions.append(PositionTuple)


                if CurrentTimeInMyTimezone >= ListOfPositions[0][0]:

                    for i in range (0, len(ListOfPositions)):
                        print(ListOfPositions[i][2])
                        settings.lcd.clear()
                        PastAzimuth = str(ListOfPositions[i-1][1])
                        CurAzimuth = str(ListOfPositions[i][1])
                        TurnAzimuth = abs(float(PastAzimuth)-float(CurAzimuth))

                        PastElev = str(ListOfPositions[i-1][2])
                        CurElev = str(ListOfPositions[i][2])
                        TurnElev = abs(float(PastElev)-float(CurElev))
                        settings.lcd.putstr("az: " + CurAzimuth + "        el: " + CurElev)


                        if PastAzimuth > CurAzimuth and i>0:
                            Motors.rotate_azimuth_slew(TurnAzimuth, "ccw", 8)
                            print("tocim proti")
                            
                        elif PastAzimuth < CurAzimuth and i > 0:
                            Motors.rotate_azimuth_slew(TurnAzimuth, "cw", 8)
                            print("tocim po")


                        if PastElev > CurElev  and i>0:
                            Motors.rotate_elevation_slew(TurnElev, "cw", 8)
                        elif PastElev < CurElev and i>0:
                            Motors.rotate_elevation_slew(TurnElev, "ccw", 8)

                        else:
                            continue


                        if ListOfPositions[i][2] < 0:

                            Pass_start.pop(0)
                            settings.lcd.clear()
                            settings.lcd.putstr("Pass is over")
                            print("Pass is over")
                            utime.sleep(3)
                            return

                        utime.sleep(1)

def DownloadForDesiredPass_loop():
    while True:
        DownloadForDesiredPass()




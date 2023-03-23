import machine
import ujson
import utime, time
import math
import urequests

import ntptime
import GPS
import Motors
import settings


licenseKey = "TLX2JG-94DFXJ-K57JEF-4XB1"
MinElevation = "0"
DaysPrediction = "2"
ObserverAltitude = "0"
latitude = "49.3125"
longitude = "17.3750"

filename = "satelity.json"

#
# licenseKey = "TLX2JG-94DFXJ-K57JEF-4XB1"
# MinElevation = "0"
# DaysPrediction = "2"
# ObserverAltitude = "0"
# latitude = GPS.latitude
# longitude = GPS.longitude
#
# filename = "satelity.json"


RadioSatellites =["49402"]#,"53385"]#["43678","53385","25544", "53462", "51085", "49396",

def DownloadAPI():
    #stahuju data, kdy nastane dalsi prelet
    global Pass_start, Pass_end, Satname
    Pass_start = {}
    Pass_end = {}
    Satname = {}

    settings.lcd.clear()
    settings.lcd.putstr("Downloading satellite data")
    settings.lcd.blink_cursor_on()

    for satID in RadioSatellites:
        url = "https://api.n2yo.com/rest/v1/satellite/radiopasses/" + satID + "/" + latitude + "/" + longitude + "/" + ObserverAltitude + "/" + DaysPrediction + "/" + MinElevation + "/&apiKey=" + licenseKey
        print(url)
        GetPasses = urequests.get("https://api.n2yo.com/rest/v1/satellite/radiopasses/" + satID + "/" + latitude +"/"+ longitude + "/" + ObserverAltitude + "/" + DaysPrediction + "/" + MinElevation + "/&apiKey=" + licenseKey)

        GetPasses_json = GetPasses.json()

        SatName = ujson.dumps(GetPasses_json["info"]["satname"])

        for JsonValue in GetPasses_json['passes']:

            StartUTC = ujson.dumps(JsonValue["startUTC"])
            EndUTC = ujson.dumps(JsonValue["endUTC"])

            JsonValue = str(JsonValue)
            nickname = satID+"_"+JsonValue

            Pass_start[nickname]= int(StartUTC)
            Pass_end[nickname] = int(EndUTC)
            Satname[nickname] = str(SatName)
            


    Sorted_Pass_start = sorted(Pass_start.items(), key=lambda x:x[1])
    Pass_start = Sorted_Pass_start

    #print("satlit leti v" +str(Pass_start))
    #print(Pass_end)






def DownloadForDesiredPass():
    global CurrentSatId, CurrentSatName

    RawID = Pass_start[0][0]
    parts = RawID.split("_")
    CurrentSatId = parts[0]
    CurrentSatName = str(Satname[RawID])

    UNIX_start = Pass_start[0][1] #toto taky
    UNIX_end = Pass_end[RawID]

    # print(UNIX_start)
    # print(UNIX_end)

    Begin = int(UNIX_start)
    Begin = Begin + (settings.DaylightSaving + settings.timezone) *3600

    End = int(UNIX_end)
    End = End + (settings.DaylightSaving + settings.timezone) *3600


    PassDuration = End - Begin
    #print(PassDuration)

    PassDuration = str(PassDuration)

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
        #settings.lcd.putstr("for+PassDuration)
        utime.sleep(1)

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


                if CurrentTimeInMyTimezone >= ListOfPositions[0][0]: #bylo tam utime.time

                    for i in range (0, len(ListOfPositions)):
                        print(ListOfPositions[i][2])
                        settings.lcd.clear()
                        PastAzimuth = str(ListOfPositions[i-1][1])
                        CurAzimuth = str(ListOfPositions[i][1])
                        TurnAzimuth = abs(float(PastAzimuth)-float(CurAzimuth))

                        PastElev = str(ListOfPositions[i-1][2])
                        CurElev = str(ListOfPositions[i][2])
                        settings.lcd.putstr("az: " + CurAzimuth + "        el: " + CurElev)

                        if PastAzimuth < CurAzimuth:
                            Motors.move_stepper(TurnAzimuth, "anticlockwise")
                        elif PastAzimuth > CurAzimuth:
                            Motors.move_stepper(TurnAzimuth, "clockwise")




                        if ListOfPositions[i][2] < 0:

                            #PositionInList = PositionInList +1s
                            Pass_start.pop(0)
                            #Pass_end.pop(RawID)
                            #CurrentSatName.pop(RawID)
                            print("Pass is over")
                            return

                        utime.sleep(1)



def DownloadForDesiredPass_loop():
    while True:
        DownloadForDesiredPass()



machine.freq(240000000)

ntptime.settime()
DownloadAPI()
while True:
    DownloadForDesiredPass_loop()


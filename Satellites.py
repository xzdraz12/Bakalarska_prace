import json

import ujson
import utime, time
import math
import urequests

import settings

licenseKey = "TLX2JG-94DFXJ-K57JEF-4XB1"
MinElevation = "0"
DaysPrediction = "2"
ObserverAltitude = "0"
latitude = "49.3125"
longitude = "17.3750"

filename = "satelity.json"



RadioSatellites =["42792"]#, "53385"]["43678","53385","25544", "53462", "51085", "49396",

def DownloadAPI():
    #stahuju data, kdy nastane dalsi prelet
    global Pass_start, Pass_end, Satname
    Pass_start = {}
    Pass_end = {}
    Satname = {}

    for satID in RadioSatellites:
        url = "https://api.n2yo.com/rest/v1/satellite/radiopasses/" + satID + "/" + latitude + "/" + longitude + "/" + ObserverAltitude + "/" + DaysPrediction + "/" + MinElevation + "/&apiKey=" + licenseKey
        print(url)
        GetPasses = urequests.get("https://api.n2yo.com/rest/v1/satellite/radiopasses/" + satID + "/" + latitude +"/"+ longitude + "/" + ObserverAltitude + "/" + DaysPrediction + "/" + MinElevation + "/&apiKey=" + licenseKey).text

        GetPasses_json = ujson.loads(GetPasses) # z url stringu udela json
        x1 = GetPasses_json["info"]["satid"] # ziska satid abych ho mohl dat to vlastniho jsonu

        passecount = GetPasses_json["info"]["passescount"] #zjisti kolik preletu v budoucnu bude

        helplist = [] #abych mohl iterovat pres pocet preletu

        for i in range (0, passecount):     #list naplnim
            helplist.append(i)

        SatName = ujson.dumps(GetPasses_json["info"]["satname"])
        for x in helplist:
            StartUTC = ujson.dumps(GetPasses_json["passes"][x]["startUTC"])
            EndUTC = ujson.dumps(GetPasses_json["passes"][x]["endUTC"])
            
            x=str(x)
            nickname = satID+"_"+x

            Pass_start[nickname]= int(StartUTC) #zkousel jsem tu pridat int
            Pass_end[nickname] = int(EndUTC)
            Satname[nickname] = str(SatName)

    Sorted_Pass_start = sorted(Pass_start.items(), key=lambda x:x[1])
    Pass_start = Sorted_Pass_start


def DownloadForDesiredPass():
    #print(Pass_start)

    #RawID = list(Pass_start.keys())[0]
    # print(parts)
    # parts = RawID.split("_")

    RawID = Pass_start[0][0]
    parts = RawID.split("_")
    CurrentSatId = parts[0]
    CurrentSatName = str(Satname[RawID])

    UNIX_start = Pass_start[0][1] #toto taky
    UNIX_end = Pass_end[RawID]
    #print(CurrentSatId)
    print(UNIX_start)
    print(UNIX_end)

    #Begin = int(Pass_start[RawID])
    Begin = int(UNIX_start)
    Begin += settings.timezone * 2*3600


    #End = int(Pass_end[RawID])
    End = int(UNIX_end)
    End += settings.timezone * 2*3600


    PassDuration = End - Begin
    print(PassDuration)

    # if PassDuration > 300:
    #     OK_Time = int((PassDuration - 300)/2)
    #     Begin = Begin + OK_Time
    #     End = End - OK_Time
    #     PassDuration = End-Begin

    PassDuration = str(PassDuration)

    while True:

        #timezone = settings.timezone

        Current_time_in_timezone = time.time() + (settings.timezone * 3600)

        print(Current_time_in_timezone)
        
        TimeToPass = Begin - Current_time_in_timezone

        Hours_float = TimeToPass / 3600

        Minutes, Hours = math.modf(Hours_float)

        Hours = str(int(Hours))
        
        Minutes_OK = (60 * Minutes)

        Seconds = Minutes_OK % 1

        Minutes_OK = str(int(Minutes_OK))

        Seconds_OK = str(int(60 * Seconds))

        print(Current_time_in_timezone)
        print(TimeToPass)

        if Current_time_in_timezone > End:
            print("Bad Timezone")
            print("use settings to adjust timezone")

            settings.lcd.clear()
            settings.lcd.putstr("Bad timezone")
            utime.sleep(1)
            settings.lcd.clear()
            settings.lcd.putstr("use settings to adjust the timezone")
            break

        # elif Current_time_in_timezone < End and Current_time_in_timezone > Begin :
        #
        #     settings.lcd.clear()
        #     settings.lcd.putstr(CurrentSatName+" LOS in: ")
        #     settings.lcd.putstr((TimeToPass*(-1)))


        settings.lcd.clear()
        settings.lcd.putstr(CurrentSatId+"in:     ")
        settings.lcd.putstr(Hours + ":" + Minutes_OK + ":" + Seconds_OK)
        utime.sleep(5)

        if TimeToPass <= 15:
            url = "https://api.n2yo.com/rest/v1/satellite/positions/" + CurrentSatId + "/" + latitude + "/" + longitude + "/" + ObserverAltitude + "/" + "35" + "/&apiKey=" + licenseKey
            GetPositions = urequests.get(url, stream = True).text

            print(GetPositions)

            GetPositions_json = ujson.loads(GetPositions)
            global ListOfPositions
            ListOfPositions = []
            hilfelist = []

            for i in range(0, 30):  # list naplnim
                hilfelist.append(i)

            for x in hilfelist:
                timestamp = int(ujson.dumps(GetPositions_json["positions"][x]["timestamp"]))
                timestamp = timestamp + (3600 * settings.timezone)
                azimuth = float(ujson.dumps(GetPositions_json["positions"][x]["azimuth"]))
                elevation = float(ujson.dumps(GetPositions_json["positions"][x]["elevation"]))

                PositionTuple = (timestamp, azimuth, elevation)
                ListOfPositions.append(PositionTuple)

            while True:
                if utime.time() == ListOfPositions[1][0]:

                    for i in hilfelist:
                        print(ListOfPositions[i][2])
                        settings.lcd.clear()
                        CurAzimuth = str(ListOfPositions[i][1])
                        CurElev = str(ListOfPositions[i][2])
                        settings.lcd.putstr("az: " + CurAzimuth + "        el: " + CurElev)

                        utime.sleep(1)

                    break
            break

         

def test():
    url = "https://api.n2yo.com/rest/v1/satellite/positions/" + "39469" + "/" + latitude + "/" + longitude + "/" + ObserverAltitude + "/" + "40" + "/&apiKey=" + licenseKey

    GetPositions = urequests.get(url, stream = True).text

    # with open("test.txt","a") as f:
    #     f.write(GetPositions)
    #     f.close()
    #
    # print(url)
    #
    # with open("test.txt" ,"r") as f:
    #     obsah=f.read()
    #     print("tady")
    #     print(obsah)
    #
    #     f.close()


    GetPositions_json = ujson.loads(GetPositions)
    global ListOfPositions
    ListOfPositions = []
    hilfelist = []

    for i in range(0, 30):  # list naplnim
        hilfelist.append(i)

    for x in hilfelist:
        timestamp = int(ujson.dumps(GetPositions_json["positions"][x]["timestamp"]))
        timestamp = timestamp + (3600 * settings.timezone)
        azimuth = float(ujson.dumps(GetPositions_json["positions"][x]["azimuth"]))
        elevation = float(ujson.dumps(GetPositions_json["positions"][x]["elevation"]))



        PositionTuple = (timestamp, azimuth, elevation)
        ListOfPositions.append(PositionTuple)

    while True:
        if utime.time() == ListOfPositions[1][0]:

            for i in hilfelist:
                print(ListOfPositions[i][2])
                settings.lcd.clear()
                CurAzimuth = str(ListOfPositions[i][1])
                CurElev = str(ListOfPositions[i][2])
                settings.lcd.putstr("az: " + CurAzimuth + "        el: " + CurElev)

                utime.sleep(1)

            break
        break
    # Pass_start.pop(1)
    # Pass_end.pop[DownloadForDesiredPass.RawID]
    # CurrentSatName.pop(RawID)


#DownloadAPI()
#DownloadForDesiredPass()

test()
# Sorted_Pass_start_DICT = dict(Sorted_Pass_start)

# print(Sorted_Pass_start[1][1])
# print(Sorted_Pass_start_DICT)

# Pass_startok = dict(Sorted_Pass_start)


# print(Pass_startok)

# Sorted_Pass_end = sorted(Pass_end.items(), key=lambda x: x[1])
# Pass_end = Sorted_Pass_end
# print(Sorted_Pass_end)

# Pass_end_OK = dict(Sorted_Pass_end)


# Pass_start = {k: v for k, v in sorted(Pass_start.items(), key=lambda v:v[1])}
# Pass_end = {k: v for k, v in sorted(Pass_end.items(), key=lambda v:v[1])}

# print(Pass_start)

# print(Pass_start_OK)
# print("...")
# print(Pass_end_OK)
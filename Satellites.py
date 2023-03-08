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
latitude = "45.0777"
longitude = "16.6677"

filename = "satelity.json"

GetPositionEach = 1 #sekundy

RadioSatellites = ["47319"]#"53385","25544", "53462", "51085", "49396", "42759"]#, "53385"]

def write_json(data):
    with open (filename, "w") as f:
        ujson.dump(data, f, indent=4)

def DownloadAPI():
    #stahuju data, kdy nastane dalsi prelet
    global Pass_start, Pass_end
    Pass_start = {}
    Pass_end = {}

    for satID in RadioSatellites:
        url = "https://api.n2yo.com/rest/v1/satellite/radiopasses/" + satID + "/" + latitude + "/" + longitude + "/" + ObserverAltitude + "/" + DaysPrediction + "/" + MinElevation + "/&apiKey=" + licenseKey
        print(url)
        GetPasses = urequests.get("https://api.n2yo.com/rest/v1/satellite/radiopasses/" + satID + "/" + latitude +"/"+ longitude + "/" + ObserverAltitude + "/" + DaysPrediction + "/" + MinElevation + "/&apiKey=" + licenseKey).text

        GetPasses_json = ujson.loads(GetPasses) # z url stringu udela json
        x1 = GetPasses_json["info"]["satid"] # ziska satid abych ho mohl dat to vlastniho jsonu
        x1_d = ujson.dumps(x1)
        passecount = GetPasses_json["info"]["passescount"] #zjisti kolik preletu v budoucnu bude

        helplist = [] #abych mohl iterovat pres pocet preletu

        for i in range (0, passecount):     #list naplnim
            helplist.append(i)

        #"StartUTCs" + x1_d = []
        for x in helplist:
            StartUTC = ujson.dumps(GetPasses_json["passes"][x]["startUTC"])
            EndUTC = ujson.dumps(GetPasses_json["passes"][x]["endUTC"])

            #print(EndUTC)
            x=str(x)
            name = satID+"_"+x

            Pass_start[name]= int(StartUTC) #zkousel jsem tu pridat int
            Pass_end[name] = int(EndUTC)



    Sorted_Pass_start = dict(sorted(Pass_start.items(), key=lambda x:x[1]))

    print(Sorted_Pass_start)

    #Pass_startok = dict(Sorted_Pass_start)


    #print(Pass_startok)




    #Sorted_Pass_end = sorted(Pass_end.items(), key=lambda x: x[1])

    #print(Sorted_Pass_end)

    #Pass_end_OK = dict(Sorted_Pass_end)





    # Pass_start = {k: v for k, v in sorted(Pass_start.items(), key=lambda v:v[1])}
    # Pass_end = {k: v for k, v in sorted(Pass_end.items(), key=lambda v:v[1])}

    #print(Pass_start)

    # print(Pass_start_OK)
    # print("...")
    # print(Pass_end_OK)
    



def DownloadForDesiredPass():
    print(Pass_start)
    RawID = list(Pass_start.keys())[0]
    #print(parts)
    parts = RawID.split("_")
    CurrentSatId = parts[0]
    #print(CurrentSatId)

    Begin = int(Pass_start[RawID])
    Begin += settings.timezone * 3600


    End = int(Pass_end[RawID])
    End += settings.timezone * 3600


    PassDuration = End - Begin

    if PassDuration > 300:
        OK_Time = int((PassDuration - 300)/2)
        Begin = Begin + OK_Time
        End = End - OK_Time
        PassDuration = End-Begin
        #print(OK_Pass_Duration)
        #OK_Pass_Duration = PassDuration

    PassDuration = str(PassDuration)

    url = "https://api.n2yo.com/rest/v1/satellite/positions/"+CurrentSatId+"/"+latitude+"/"+longitude+"/"+ObserverAltitude+"/"+PassDuration+"/&apiKey="+licenseKey
    print(url)

    # Pass_start.pop(CurrentSatId)
    # Pass_end.pop(CurrentSatId)

    while True:

        Current_time_in_timezone = time.time() + (settings.timezone * 3600)
        TimeToPass = Begin - Current_time_in_timezone

        Hours_float = TimeToPass / 3600

        Minutes, Hours = math.modf(Hours_float)

        Hours = str(int(Hours))
        
        Minutes_OK = (60 * Minutes)

        Seconds = Minutes_OK % 1



        Minutes_OK = str(int(Minutes_OK))

        Seconds_OK = str(int(60 * Seconds))

        print(Hours)
        print(Minutes_OK)
        print(Seconds_OK)


        settings.lcd.clear()
        settings.lcd.putstr("Next Flyby of " + CurrentSatId + " in: ")
        settings.lcd.putstr(Hours + ":" + Minutes_OK + ":" + Seconds_OK)
        utime.sleep(1)

        if TimeToPass <= 10:
            break







            


DownloadAPI()
#DownloadForDesiredPass()
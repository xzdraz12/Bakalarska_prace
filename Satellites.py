import json

import ujson
import utime

import urequests


licenseKey = "TLX2JG-94DFXJ-K57JEF-4XB1"
MinElevation = "30"
DaysPrediction = "2"
ObserverAltitude = "0"
latitude = "45.0777"
longitude = "16.6677"

filename = "satelity.json"

GetPositionEach = 1 #sekundy

RadioSatellites = ["25544", "53462"]#, "53385"]

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

            Pass_start[name]=StartUTC
            Pass_end[name] = EndUTC



    Pass_start = {k: v for k, v in sorted(Pass_start.items(), key=lambda v:v[1])}
    Pass_end = {k: v for k, v in sorted(Pass_end.items(), key=lambda v:v[1])}


def DownloadForDesiredPass():


DownloadAPI()
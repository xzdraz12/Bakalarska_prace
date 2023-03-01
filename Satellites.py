import json

import GPS
import urequests


licenseKey = "TLX2JG-94DFXJ-K57JEF-4XB1"
MinElevation = "30"
DaysPrediction = "1"
ObserverAltitude = "0"
VisibleSatellites=[]
latitude = "45.0777"
longitude = "16.6677"

def DownloadAPI():
    RawSatellites = urequests.get("https://api.n2yo.com/rest/v1/satellite/radiopasses/25544/"+latitude+"/"+longitude+"/"+ObserverAltitude+"/"+DaysPrediction+"/"+MinElevation+"/&apiKey="+licenseKey+")")
    print("stahuju")
    sat_json = json.loads(RawSatellites.read())
    print(sat_json)


DownloadAPI()
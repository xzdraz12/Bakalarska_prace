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
    for satID in RadioSatellites:
        url = "https://api.n2yo.com/rest/v1/satellite/radiopasses/" + satID + "/" + latitude + "/" + longitude + "/" + ObserverAltitude + "/" + DaysPrediction + "/" + MinElevation + "/&apiKey=" + licenseKey
        print(url)
        GetPasses = urequests.get("https://api.n2yo.com/rest/v1/satellite/radiopasses/" + satID + "/" + latitude +
                                  "/"+ longitude + "/" + ObserverAltitude + "/" + DaysPrediction + "/" + MinElevation + "/&apiKey=" + licenseKey).text

        GetPasses_json = ujson.loads(GetPasses)


        x1 = GetPasses_json["info"]["satid"]

        passecount = GetPasses_json["info"]["passescount"]

        test = ujson.dumps(passecount)

        #OneSat = GetPasses_json["passes"]

        print(passecount)

        # Remaded ="{"+x1+":}"

        for x in test:
            x=0
            x2 = GetPasses_json["passes"][x]["startUTC"]
            print(x2)

            





        # with open("satelity.json", "w") as f:
        #     NiceFormat = ujson.dumps(GetPasses_json)
        #
        #
        #     print(NiceFormat[2]["info"]["satid"])



            # for satID in RadioSatellites:
            #     f.write(NiceFormat)
            # f.close()


        utime.sleep(2)


        # with open("satelity.json", "r") as file:
        #      ujson.load(file)






        #print(temp)


        #print(pekny["info"]["satid"])



        # for i < GetPasses_json["passes"].délka:
        # #     print("\n", GetPasses_json["passes"][i]["startAz"])
        #
        # for Pass in GetPasses_json:
        #     Pass = 1
        #     print(GetPasses_json["passes"][Pass]["startAz"])
        #     Pass += 1
            
        utime.sleep(2)

# def EachPassData():
#     StartTime = DownloadAPI().RawSatellites["startUTC"]
#     EndTime = DownloadAPI().RawSatellites["endUTC"]
#
#     utime.sleep(1)
#
#     # ted stahnu data o jednotlivych preletech
#     EachPassData = urequests.get(
#         "https://api.n2yo.com/rest/v1/satellite/positions/" + DownloadAPI().satID + "/" + latitude + "/" + longitude + "/" + ObserverAltitude + "/2/&apiKey=" + licenseKey).text
#
#     print(EachPassData)
#


DownloadAPI()
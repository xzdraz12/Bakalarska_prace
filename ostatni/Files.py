import requests, json


class Files():
    def GetPositionsForNextFlyby(SatID):
        with open(SatID, 'r') as flybyfile:
            FlybyData = json.load(flybyfile)

            NumberOfFlybys = len(FlybyData['passes'])

            i = 1
            for i in NumberOfFlybys:
                StartUnixTime = FlybyData['startUTC'][i]['passes']
                EndUnixTime = FlybyData['endUTC'][i]['passes']
                SecondsToPredict = EndUnixTime - StartUnixTime

                HttpRequest = "https://api.n2yo.com/rest/v1/satellite/positions/" + SatID + "/" + latitude + "/" + longitude + "/" + Observer_elevation + "/" + SecondsToPredict + "/&apiKey=TLX2JG-94DFXJ-K57JEF-4XB1"

                response = requests.get(HttpRequest)

                FileName = SatID + "FlybyStartsAt" + StartUnixTime

                Files.SaveToTXT("GetPositionsForNextFlyby", FileName, response)

        flybyfile.close()

    def APIRequestForFutureFlybys(SatID):
        global MinElev, DaysAhead

        HttpRequest = "https://api.n2yo.com/rest/v1/satellite/radiopasses/" + SatID + "/" + latitude + "/" + longitude + "/" + Observer_elevation + "/" + DaysAhead + "/" + MinElev + "/&apiKey=TLX2JG-94DFXJ-K57JEF-4XB1"

        response = requests.get(HttpRequest)

        SaveToTXT(SatID, response)

    def SaveToTXT(FileName, Text):
        with open(FileName, 'r+w') as f:
            f.truncate(0)
            f.write(Text)

        f.close()

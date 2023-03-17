import machine
import ujson
import utime, time
import math
import urequests
import _thread

import GPS
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


RadioSatellites =["25544"]#,"53385"]#["43678","53385","25544", "53462", "51085", "49396",

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
    global CurrentSatId, CurrentSatName
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
        utime.sleep(1)

        if TimeToPass <= 15:
            while True:
                url = "https://api.n2yo.com/rest/v1/satellite/positions/" + CurrentSatId + "/" + latitude + "/" + longitude + "/" + ObserverAltitude + "/" + "10" + "/&apiKey=" + licenseKey
                GetPositions = urequests.get(url).text

                #print(GetPositions)

                GetPositions_json = ujson.loads(GetPositions)
                global ListOfPositions
                ListOfPositions = []
                hilfelist = []

                for i in range(0, 10):  # list naplnim
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
                        break

                if utime.time()==End:
                    Pass_start.pop(1)
                    Pass_end.pop[DownloadForDesiredPass.RawID]
                    CurrentSatName.pop(RawID)
                    break









def DownloadPassandPrint():
    url = "https://api.n2yo.com/rest/v1/satellite/positions/" + CurrentSatId + "/" + latitude + "/" + longitude + "/" + ObserverAltitude + "/" + "10" + "/&apiKey=" + licenseKey
    GetPositions = urequests.get(url).text

    print(GetPositions)

    GetPositions_json = ujson.loads(GetPositions)
    global ListOfPositions
    ListOfPositions = []
    hilfelist = []

    for i in range(0, 10):  # list naplnim
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
            Pass_start.pop(1)
            Pass_end.pop[DownloadForDesiredPass.RawID]
            CurrentSatName.pop(DownloadForDesiredPass().RawID)






def DownloadPass_test(): #core 1

    global PositionTuple, ListOfPositions1, ListOfPositions2, TemporaryList, EmptyStatus1, EmptyStatus2

    EmptyStatus1 = True
    EmptyStatus2 = True

    while True:
        ListOfPositions1 = []
        ListOfPositions2 = []

        TemporaryList = []

        seconds = "10"
        url = "https://api.n2yo.com/rest/v1/satellite/positions/" + CurrentSatId + "/" + latitude + "/" + longitude + "/" + ObserverAltitude + "/" + seconds + "/&apiKey=" + licenseKey
        GetPositions = urequests.get(url).text
        GetPositions_json = ujson.loads(GetPositions)

        hilfelist = []

        for i in range(0, int(seconds)):  # list naplnim

            hilfelist.append(i)

        if EmptyStatus2 == True:
            for x in hilfelist:
                timestamp = int(ujson.dumps(GetPositions_json["positions"][x]["timestamp"]))
                timestamp = timestamp + (3600 * settings.timezone)
                azimuth = float(ujson.dumps(GetPositions_json["positions"][x]["azimuth"]))
                elevation = float(ujson.dumps(GetPositions_json["positions"][x]["elevation"]))

                PositionTuple = (timestamp, azimuth, elevation)
                ListOfPositions1.append(PositionTuple)
                # print("funguju1")
            # helpValue= helpValue +1
            EmptyStatus1 = False
            break

        elif EmptyStatus1 == True:
            for x in hilfelist:
                timestamp = int(ujson.dumps(GetPositions_json["positions"][x]["timestamp"]))
                timestamp = timestamp + (3600 * settings.timezone)
                azimuth = float(ujson.dumps(GetPositions_json["positions"][x]["azimuth"]))
                elevation = float(ujson.dumps(GetPositions_json["positions"][x]["elevation"]))

                PositionTuple = (timestamp, azimuth, elevation)
                ListOfPositions2.append(PositionTuple)

                # print("gfunguju2")
            # helpValue= helpValue +1
            EmptyStatus2 = False

            break

        utime.sleep(10)


machine.freq(240000000)
DownloadAPI()

while True:

    DownloadForDesiredPass()

# def PrintPositions():
#
#     while True:
#         helpvalue2 = 0
#
#         if helpvalue2 %2 == 0:
#             while ListOfPositions1[0][0] < utime.time():
#                 print("pop1")
#                 ListOfPositions1.pop(0)
#
#             if utime.time() == ListOfPositions1[0][0]:
#
#                 for i in range (0,len(ListOfPositions1)):
#
#                     print(ListOfPositions1[i][2])
#                     settings.lcd.clear()
#                     CurAzimuth = str(ListOfPositions1[i][1])
#                     CurElev = str(ListOfPositions1[i][2])
#                     settings.lcd.putstr("az1: " + CurAzimuth + "        el: " + CurElev)
#                     utime.sleep(1)
#
#             helpvalue2+=1
#             EmptyStatus1 = True
#             break
#
#
#         elif helpvalue2 %2 == 1:
#             while ListOfPositions2[0][0] < utime.time():
#                 print("pop2")
#                 ListOfPositions2.pop(0)
#
#             if utime.time() == ListOfPositions2[0][0]:
#
#                 for i in range (0, len(ListOfPositions2)):
#                     print(ListOfPositions2[i][2])
#                     settings.lcd.clear()
#                     CurAzimuth = str(ListOfPositions2[i][1])
#                     CurElev = str(ListOfPositions2[i][2])
#                     settings.lcd.putstr("az2: " + CurAzimuth + "        el: " + CurElev)
#
#                     utime.sleep(1)
#             helpvalue2 +=1
#             EmptyStatus2 = True
#
#             #break
#






























    # Pass_start.pop(1)
    # Pass_end.pop[DownloadForDesiredPass.RawID]
    # CurrentSatName.pop(RawID)




# def ControlList():
#     for x in range (0, len(ListOfPositions)):
#         number = x+1
#         if ListOfPositions[number][0] < ListOfPositions[x]:
#             ListOfPositions.pop(number)







        #
        #     TemporaryList.append(PositionTuple)
        #
        #     if x == 0:
        #         TemporaryList = ListOfPositions
        #
        #
        #     #print(TemporaryList)
        #     #print(TemporaryList[0][0])
        #
        # if TemporaryList[0][0] < ListOfPositions[lenght][0] and x > 0:
        #
        #     deleteItems = ListOfPositions[lenght][0] - TemporaryList[0][0] - 1
        #
        #     for i in range(0, deleteItems):
        #         TemporaryList.pop(i)
        #
        #     ListOfPositions.append(TemporaryList)
        #     print(ListOfPositions)
        #
        #
        #
        # utime.sleep(2)

















            # if TemporaryList[jsonValue["timestamp"]] == ListOfPositions[jsonValue["timestamp"]]:
            #     TemporaryList.pop(PositionTuple)
            #
            # else:
            #     ListOfPositions.append(PositionTuple)

        # for i in range(40):
        #     # print(ListOfPositions[i])
        #     CurAzimuth = str(ListOfPositions[i][1])
        #     CurElev = str(ListOfPositions[i][2])






        # global PositionTuple, ListOfPositions
        #
        # seconds = "40"
        # url = "https://api.n2yo.com/rest/v1/satellite/positions/" + "39469" + "/" + latitude + "/" + longitude + "/" + ObserverAltitude + "/" + seconds + "/&apiKey=" + licenseKey
        # GetPositions = urequests.get(url).text
        # GetPositions_json = ujson.loads(GetPositions)
        #
        # ListOfPositions = []
        # hilfelist = []
        #
        # for i in range(0, 30):  # list naplnim
        #     hilfelist.append(i)
        #
        # for x in hilfelist:
        #     timestamp = int(ujson.dumps(GetPositions_json["positions"][x]["timestamp"]))
        #     timestamp = timestamp + (3600 * settings.timezone)
        #     azimuth = float(ujson.dumps(GetPositions_json["positions"][x]["azimuth"]))
        #     elevation = float(ujson.dumps(GetPositions_json["positions"][x]["elevation"]))
        #
        #     PositionTuple = (timestamp, azimuth, elevation)
        #     ListOfPositions.append(PositionTuple)
        #
        # utime.sleep(10)

#def PrintPass():









    # while True:
    #     if utime.time() == ListOfPositions[1][0]:
    #
    #         for i in len(ListOfPositions):
    #             print(ListOfPositions[i][2])
    #             settings.lcd.clear()
    #             CurAzimuth = str(ListOfPositions[i][1])
    #             CurElev = str(ListOfPositions[i][2])
    #             settings.lcd.putstr("az: " + CurAzimuth + "        el: " + CurElev)
    #
    #             utime.sleep(1)
    #
    #         break
    #     break
    # # Pass_start.pop(1)
    # # Pass_end.pop[DownloadForDesiredPass.RawID]
    # # CurrentSatName.pop(RawID)
# def test():
#     machine.freq(240000000)
#     seconds = "30" #zde lze menit velikost, 40 sekund zvlada, napr 50 uz ne
#     url = "https://api.n2yo.com/rest/v1/satellite/positions/39469/49.3125/17.3750/0/"+seconds+"/&apiKey=TLX2JG-94DFXJ-K57JEF-4XB1"
#     #url = "https://api.n2yo.com/rest/v1/satellite/positions/" + "39469" + "/" + latitude + "/" + longitude + "/" + ObserverAltitude + "/" + seconds + "/&apiKey=" + licenseKey
#
#
#
#     GetPositions = urequests.get(url).text
#
#     GetPositions_json = ujson.loads(GetPositions)
#
#
#     global ListOfPositions
#     ListOfPositions = []
#     hilfelist = []
#
#     for i in range(0, 30):  # list naplnim
#         hilfelist.append(i)
#
#     for x in hilfelist:
#         timestamp = int(ujson.dumps(GetPositions_json["positions"][x]["timestamp"]))
#         timestamp = timestamp + (3600 * settings.timezone)
#         azimuth = float(ujson.dumps(GetPositions_json["positions"][x]["azimuth"]))
#         elevation = float(ujson.dumps(GetPositions_json["positions"][x]["elevation"]))
#
#         PositionTuple = (timestamp, azimuth, elevation)
#         ListOfPositions.append(PositionTuple)
#
#     while True:
#         if utime.time() == ListOfPositions[1][0]:
#
#             for i in hilfelist:
#                 print(ListOfPositions[i][2])
#                 settings.lcd.clear()
#                 CurAzimuth = str(ListOfPositions[i][1])
#                 CurElev = str(ListOfPositions[i][2])
#                 settings.lcd.putstr("az: " + CurAzimuth + "        el: " + CurElev)
#
#                 utime.sleep(1)
#
#             break
#         break
#
#


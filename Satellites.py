import ujson
import utime
import math
import urequests
import GPS
import Motors
import settings
from settings import oled as oled

licenseKey = settings.licenseKey
MinElevation = settings.MinElevation
DaysPrediction = settings.DaysPrediction
# ObserverAltitude = GPS.altitude
# latitude = GPS.latitude
# longitude = GPS.longitude

RadioSatellites = settings.RadioSatellites
WeatherSatellites = settings.NOAA
ISS = settings.ISS

def DownloadAPI(list_name):

    #stahuju data, kdy nastane dalsi prelet
    global Pass_start, Pass_end, Satname, Pass_azimuth
    Pass_start = {}
    Pass_end = {}
    Pass_azimuth = {}
    Satname = {}

    oled.fill(0)
    oled.show()
    oled.text("Downloading",0,0)
    oled.text("satellite",0,10)
    oled.text("data",0,20)
    oled.show()
    print("Downloading satellite data")


    if list_name == "radio":
        SatList = RadioSatellites

    if list_name == "noaa":
        SatList = WeatherSatellites

    if list_name == "iss":
        SatList = ISS



    for satID in SatList:
        url = "https://api.n2yo.com/rest/v1/satellite/radiopasses/" + satID + "/" + GPS.latitude + "/" + GPS.longitude + "/" +GPS.altitude + "/" + DaysPrediction + "/" + MinElevation + "/&apiKey=" + licenseKey
        print(url)

        while True:
            try:
                GetPasses = urequests.get(url)
                GetPasses_json = GetPasses.json()
                break

            except Exception as e:
                print(e)
                utime.sleep(.5)
                continue

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

    oled.fill(0)
    oled.show()
    oled.text("Satellite data",0,0)
    oled.text("downloaded",0,10)
    oled.show()
    utime.sleep(2)


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

    #PassDuration = str(PassDuration)

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
        #print(TimeToPass)

        try:
            CurrentTimeInMyTimezone > End

        except:

            oled.fill(0)
            oled.show()
            oled.text("Bad timezone", 0, 0)
            oled.text("Adjust", 0, 10)
            oled.text("timezone", 0, 20)
            oled.show()

            print("Bad Timezone")
            print("use settings to adjust timezone")
            break

        oled.fill(0)
        oled.show()
        oled.text(CurrentSatName, 0, 0)
        oled.text("AOS in "+Hours+":"+Minutes_OK+":"+Seconds_OK, 0, 10)
        #oled.text(Hours+":"+Minutes_OK+":"+Seconds_OK,0,20)
        oled.show()
        utime.sleep(1)
        oled.fill(0)
        oled.show()

        print(CurrentSatName)
        print("in :")
        print(Hours+":"+Minutes_OK+":"+Seconds_OK)

        if SlewOnlyOnce == True and TimeToPass <=50:

            #oled.fill(0)
            #oled.show()
            oled.text("Slewing into",0,0)
            oled.text("start position",0,10)
            oled.show()

            print("Slewing into start position")

            Motors.rotate_azimuth_change_speed(StartAZ, "cw", settings.microstepping)

            oled.fill(0)
            oled.show()

            SlewOnlyOnce = False

        if TimeToPass <= 5:

            AZ_pass_dif = 0
            EL_pass_dif = 0

            while True:

                while True:
                    try:
                        url = "https://api.n2yo.com/rest/v1/satellite/positions/" + CurrentSatId + "/" + GPS.latitude + "/" + GPS.longitude + "/" + GPS.altitude + "/" + "35" + "/&apiKey=" + licenseKey
                        GetPositions = urequests.get(url)
                        GetPositions_json = GetPositions.json()
                        break

                    except Exception as e:
                        print(e)
                        utime.sleep(.5)
                        continue


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

                        oled.fill(0)
                        oled.show()

                        PastAzimuth = ListOfPositions[i-1][1]
                        CurAzimuth = ListOfPositions[i][1]
                        AZ_step_dif = (abs(CurAzimuth-PastAzimuth))%360

                        PastElev = ListOfPositions[i-1][2]
                        CurElev = ListOfPositions[i][2]
                        EL_step_dif = (abs(CurElev-PastElev))%360

                        PassDuration = PassDuration-1

                        oled.text(CurrentSatName,0,0)
                        oled.text("Az:"+str(CurAzimuth),0,10)
                        oled.text("El:"+str(CurElev),0,20)
                        oled.text("LOS in "+str(convert_seconds(PassDuration)[0])+":"+str(convert_seconds(PassDuration)[1])+":"+str(convert_seconds(PassDuration)[2]),0,30)
                        oled.show()

                        print("Az: "+str(CurAzimuth))
                        print("El: "+str(CurElev))
                        print("back az: "+str(AZ_pass_dif))
                        print("back el: "+str(EL_pass_dif))

                        if PastAzimuth > CurAzimuth and i>0:
                            Motors.rotate_azimuth_slew(AZ_step_dif, "ccw", 8)
                            AZ_pass_dif = AZ_pass_dif - AZ_step_dif
                            print("ccw Azimuth")

                        elif PastAzimuth < CurAzimuth and i > 0:
                            Motors.rotate_azimuth_slew(AZ_step_dif, "cw", 8)
                            AZ_pass_dif = AZ_pass_dif + AZ_step_dif
                            print("cw azimuth")

                        if PastElev > CurElev  and i>0:
                            Motors.rotate_elevation_slew(EL_step_dif, "cw", 8)
                            EL_pass_dif = EL_pass_dif + EL_step_dif
                            print("cw elev")

                        elif PastElev < CurElev and i>0:
                            Motors.rotate_elevation_slew(EL_step_dif, "ccw", 8)
                            EL_pass_dif = EL_pass_dif - EL_step_dif
                            print("ccw elev")
                        else:
                            continue

                        if ListOfPositions[i][2] < 0:

                            SlewBackAngle_AZ = StartAZ + AZ_pass_dif
                            SlewBackAngle_EL = 0 + EL_step_dif

                            print("start az was: "+str(StartAZ))
                            print("slewing back az"+str(SlewBackAngle_AZ))
                            print("start EL was: 0")
                            print("slewing back EL: "+str(SlewBackAngle_EL))

                            print("slewing in 5 seconds")
                            utime.sleep(5)

                            if SlewBackAngle_AZ < 0:
                                Motors.rotate_azimuth_change_speed(abs(SlewBackAngle_AZ),"cw",8)

                            elif SlewBackAngle_AZ > 0:
                                Motors.rotate_azimuth_change_speed(abs(SlewBackAngle_AZ), "ccw", 8)

                            if SlewBackAngle_EL < 0:
                                Motors.rotate_elevation_change_speed(abs(SlewBackAngle_EL),"cw",8)

                            elif SlewBackAngle_EL > 0:
                                Motors.rotate_elevation_change_speed(abs(SlewBackAngle_EL),"ccw",8)

                            else:
                                continue

                            Pass_start.pop(0)
                            oled.fill(0)
                            oled.show()
                            oled.text("Pass is over",0,0)
                            oled.show()

                            print("Pass is over")
                            utime.sleep(3)
                            oled.fill(0)
                            oled.show()
                            return

                        utime.sleep(1)

def DownloadForDesiredPass_loop():

    while settings.BTN_ENC.value() == 0:
        continue


    try:
        while True:
            DownloadForDesiredPass()
    except Exception as e:
        print(e)
        oled.fill(0)
        oled.show()
        oled.text("choose a list", 0, 0)
        oled.text("of satellites", 0, 10)
        oled.text("first", 0, 20)
        oled.text("press the button", 0, 40)
        oled.text("to continue", 0, 50)
        oled.show()

        while settings.BTN_ENC.value() == 1:
            continue

def convert_seconds(seconds):
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return hours, minutes, seconds


def calculate_angle_difference(prev, curr):
    diff = (curr - prev) % 360
    return diff
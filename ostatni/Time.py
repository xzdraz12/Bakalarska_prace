import utime, datetime,time
import GPS


class Time():
    def ConvertToUTC(EpochTime):
        UTCTime = utime.gmtime(EpochTime)
        return UTCTime

    def SetTime(self):
        RaWTime = GPS.GPStime.split(':')

        # rtc.hour = GPStime[0]
        # rtc.minute = GPStime[1]
        # rtc.second = GPStime[2]

        RaWDate = GPS.GPSdate.split('.')

        # rtc.day = RaWDate[0]
        # rtc.month = RaWDate[1]
        # rtc.year = RaWDate[2]

    def testTime(self):
        print(utime.gmtime(0))

        # print(time.localtime())

    def ConvertToUnix(self):
        CurrentTime = "15:33:00"
        RawCurrentTime = CurrentTime.split(':')
        Hour = RawCurrentTime[0]
        Minute = RawCurrentTime[1]
        Second = RawCurrentTime[2]

        GPSdate = "2022.10.6"
        RawDate = GPSdate.split('.')
        Day = RawDate[0]
        Month = RawDate[1]
        Year = RawDate[2]

        ToEpoch = datetime(Year, Month, Day, Hour, Minute, Second)

        EpochTime = time.mktime(ToEpoch.timetuple())

        print("time since epoch: " + EpochTime)

        # dateAndTime = datetime(Year, Month, Day, Hour, Minute, Second)
        # UnixTimestamp = int(dateAndTime.timestamp())
        # return UnixTimestamp








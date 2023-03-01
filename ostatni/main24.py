
while True:

    getGPS(gpsModule)

    if (FIX_STATUS == True):
        print("Printing GPS data...")
        print(" ")
        print("Latitude: " + latitude)
        print("Longitude: " + longitude)
        print("Satellites: " + satellites)
        print("Time: " + GPStime)
        print("----------------------")


        FIX_STATUS = False

    if (TIMEOUT == True):
        print("No GPS data is found.")
        TIMEOUT = False
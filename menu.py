
import utime


import settings
import GPS

#from waiting import wait

def Welcome():
    settings.lcd.putstr("Welcome")
    utime.sleep(2)
    settings.lcd.clear()
    settings.lcd.putstr("Version 2023")
    utime.sleep(2)
    settings.lcd.clear()


def GPSStatus():
    if GPS.FIX_STATUS_GPS == False:
        # while GPS.FIX_STATUS_GPS == False:

        settings.lcd.clear()
        settings.lcd.putstr("Waiting for GPS ")
        print("Waiting for GPS ")
        settings.lcd.blink_cursor_on()
        utime.sleep(.5)
        #break
        # while GPS.FIX_STATUS_GPS == False:
        # continue

    # elif GPS.FIX_STATUS_GPS == True:
    elif GPS.FIX_STATUS_GPS == True:
        settings.lcd.clear()
        settings.lcd.putstr("GPS obtained")
        print("GPS obtained ")
        utime.sleep(3)

        #break

    #while True:




        #break


   
        

    #else:
        #settings.lcd.clear()
        #settings.lcd.putstr("GPS malfunction")
        #utime.sleep(1)

def SetWifi():

    print("kk")

def ScrollMenu():

    settings.lcd.clear()
    settings.lcd.putstr("WiFi")



def menuTest():
    if settings.button.value() == 1:
        settings.lcd.clear()
        settings.led.value(1)
        settings.lcd.putstr("Tlacitko zmacknuto")
        print("tlacitko zmacnuto")
        while settings.button.value() == 1:
            continue


    else:
        settings.lcd.clear()
        settings.led.value(0)
        settings.lcd.putstr("Tlacitko pusteno")
        print("tlacitko vypnuto")
        while settings.button.value() == 0:
            continue







import machine
import GPS
import ntptime

import main
import wifi
import utime
import Satellites
import settings

from settings import oled as oled



# picklist = encoder_menu.wrap_menu([("Radio Satellites", Satellites.DownloadAPI("radio")), ("Weather Sattelites", Satellites.DownloadAPI("weather")), ("ISS", Satellites.DownloadAPI("iss"))])
# main_menu = encoder_menu.wrap_menu([("WiFi", wifi.ConnectWifi()),("GPS",GPS.GPS_info()),("Satellites",picklist)])
#

global width, height, shift, line, list_length, total_lines, highlight, previous_value, button_down, button_pin, step_pin, direction_pin

# global previous_value, step_pin

width = settings.WIDTH
height = settings.HEIGHT
shift = 0
line = 1
list_length = 0
total_lines = 6
highlight = 1

button_pin = settings.BTN_ENC
step_pin = settings.BTN_EN1
direction_pin = settings.BTN_EN2

previous_value = 1
button_down = 0


def show_current_time():
    print("tutaj")

    #while settings.BTN_ENC.value()==0:
     #   continue
    settings.BTN_ENC.irq(trigger=machine.Pin.IRQ_FALLING, handler=MenuLoop())

    while True:

        #while settings.BTN_ENC.value()==1:

        current_time = utime.localtime()
        year= current_time[0]
        month = current_time[1]
        day = current_time[2]
        hour = current_time[3]+settings.timezone
        minute = current_time[4]
        second = current_time[5]

        oled.fill(0)
        oled.show()
        oled.text("current time:",0,0)
        oled.text(str(hour)+":"+str(minute)+":"+str(second),0,10)
        oled.text("date:",0,30)
        oled.text(str(year)+"-"+str(month)+"-"+str(day),0,40)
        oled.show()

        print("Current time: {:02d}:{:02d}:{:02d}".format(hour, minute, second))
        utime.sleep(1)

        #while settings.BTN_ENC.value()==0:
            #break
        
def SetNTP():
    while True:
        try:
            oled.fill(0)
            oled.show()
            oled.text("Obtaining time", 0, 0)
            oled.text("from NTP", 0, 10)
            oled.text("server", 0, 20)
            oled.show()
            utime.sleep(1)
            ntptime.settime()
            break

        except Exception as e:
            print(e)
            utime.sleep(1)
            continue

def Welcome():
    print("Welcome")
    print("Version 2023")
    print("Jakub Zdrazil")

    oled.text("Welcome", 0, 0)
    oled.text("Version 2023", 0, 10)
    oled.text("Jakub Zdrazil", 0, 20)
    oled.show()
    utime.sleep(2)
    oled.fill(0)
    oled.show()

def GetFiles():
    menu = []
    files = ["choose RadioSat", "choose ISS", "choose NOAA", "Observe", "WiFi", "GPS", "Time"]

    for i in range(0, len(files)):
        menu.append(files[i])
    print(menu)

    return (menu)

def ShowMenu(menu):
    global line, highlight, shift, list_length, item

    item = 1
    line = 1
    line_height = 10

    oled.fill_rect(0, 0, width, height, 0)

    list_length = len(menu)
    short_list = menu[shift:shift + total_lines]

    for item in short_list:
        if highlight == line:
            oled.fill_rect(0, (line - 1) * line_height, width, line_height, 1)
            oled.text(">", 0, (line - 1) * line_height, 0)
            oled.text(item, 10, (line - 1) * line_height, 0)
            oled.show()

        else:
            oled.text(item, 10, (line - 1) * line_height, 1)
            oled.show()
        line += 1

    oled.show()

def launch(filename):
    global file_list
    oled.fill_rect(0, 0, width, height, 0)
    if filename == "choose RadioSat":
        Satellites.DownloadAPI("radio")

    if filename == "choose ISS":
        Satellites.DownloadAPI("iss")

    if filename == "choose NOAA":
        Satellites.DownloadAPI("noaa")

    if filename == "Observe":
        Satellites.DownloadForDesiredPass_loop()

    if filename == "WiFi":
        wifi.wifiStatus()

    if filename == "GPS":
        GPS.GPS_info()

    if filename == "Time":
        show_current_time()

        # Satellites.DownloadForDesiredPass_loop()

    ShowMenu(file_list)


def PreMenu():
    # uvitani
    Welcome()

    # pripojeni k WiFi
    wifi.ConnectWifi()

    # ziskani aktualniho casu
    SetNTP()

    oled.fill(0)
    oled.show()
    oled.text("NTP time", 0, 0)
    oled.text("obtained", 0, 10)
    oled.show()
    utime.sleep(2)

    print("UTC time: " + str(utime.localtime()))
    print("time from NTP server")

    # ziskani dat GPS
    GPS.GPSStatus()
    GPS.OperateGPS(GPS.gpsModule)
    GPS.GPSStatus()

    # potvrd ze je antena ve vychozi poloze
    oled.fill(0)
    oled.show()
    oled.text("Is antenna in", 0, 0)
    oled.text("a default", 0, 10)
    oled.text("position?", 0, 20)
    oled.text("Press to", 0, 40)
    oled.text("continue", 0, 50)
    oled.show()
    while settings.BTN_ENC.value() == 1:
        continue

    # Get the list of Python files and display the menu


def MenuLoop():
    global previous_value, button_down, highlight, step_pin, direction_pin, shift

    # previous_value = main.previous_value
    # button_down = main.button_down
    # highlight = main.highlight
    # step_pin = main.step_pin
    # direction_pin = main.direction_pin
    # shift = main.shift

    while True:
        if previous_value != step_pin.value():
            if step_pin.value() == 0:

                # Turned Left
                if direction_pin.value() == 0:
                    if highlight > 1:
                        highlight -= 1
                    else:
                        if shift > 0:
                            shift -= 1

                else:
                    if highlight < total_lines:
                        highlight += 1
                    else:
                        if shift + total_lines < list_length:
                            shift += 1

                ShowMenu(file_list)
            previous_value = step_pin.value()

        if button_pin.value() == False and not button_down:
            button_down = True

            print("Launching", file_list[highlight - 1 + shift])

            # execute script
            launch(file_list[(highlight - 1) + shift])

            print("Returned from launch")

        if button_pin.value() == True and button_down:
           button_down = False

PreMenu()
file_list = main.GetFiles()
ShowMenu(file_list)
MenuLoop()






    


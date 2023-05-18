
import utime

import GPS
import Satellites
import settings
import wifi
from settings import oled as oled
from settings import BTN_ENC as BTN_ENC
from settings import BTN_EN1 as BTN_EN1
from settings import BTN_EN2 as BTN_EN2
import ntptime

#promenne pro menu
width = settings.WIDTH
height = settings.HEIGHT
shift = 0
line = 1
list_length = 0
total_lines = 6
highlight = 1

button_pin = BTN_ENC
step_pin = BTN_EN1
direction_pin = BTN_EN2


previous_value = 1
button_down = 0

# picklist = encoder_menu.wrap_menu([("Radio Satellites", Satellites.DownloadAPI("radio")), ("Weather Sattelites", Satellites.DownloadAPI("weather")), ("ISS", Satellites.DownloadAPI("iss"))])
# main_menu = encoder_menu.wrap_menu([("WiFi", wifi.ConnectWifi()),("GPS",GPS.GPS_info()),("Satellites",picklist)])
#

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

    oled.text("Welcome", 0,0)
    oled.text("Version 2023", 0,10)
    oled.text("Jakub Zdrazil",0, 20)
    oled.show()
    utime.sleep(2)
    oled.fill(0)
    oled.show()

def GetFiles():
    menu = []
    files = ["Observe","WiFi", "GPS", "Group"]

    for i in range(0, len(files)):
        menu.append(files[i])
    print(menu)

    return(menu)


def ShowMenu(menu):

    global line, highlight, shift, list_length, item

    item = 1
    line = 1
    line_height = 10

    oled.fill_rect(0, 0, width, height, 0)

    list_length = len(menu)
    short_list = menu[shift:shift+total_lines]

    for item in short_list:
        if highlight == line:
            oled.fill_rect(0, (line - 1) * line_height, width, line_height, 1)
            oled.text(">", 0, (line - 1) * line_height, 0)
            oled.text(item, 10, (line - 1) * line_height, 0)
            oled.show()

        else:
            oled.text(item, 10, (line-1)*line_height,1)
            oled.show()
        line += 1

    oled.show()


def launch(filename):
    global file_list
    oled.fill_rect(0, 0, width, height, 0)
    if filename == "Observe":
        Satellites.RunItAll()
        
    if filename == "WiFi":
        wifi.wifiStatus()


    if filename == "GPS":
        GPS.GPS_info()


        #Satellites.DownloadForDesiredPass_loop()

    ShowMenu(file_list)
    # Get the list of Python files and display the menu
file_list = GetFiles()
ShowMenu(file_list)

# Repeat forever
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

            # Turned Right
            else:
                if highlight < total_lines:
                    highlight += 1
                else:
                    if shift + total_lines < list_length:
                        shift += 1

            ShowMenu(file_list)
        previous_value = step_pin.value()

        # Check for button pressed
    if button_pin.value() == False and not button_down:
        button_down = True

        print("Launching", file_list[highlight - 1 + shift])

        # execute script
        launch(file_list[(highlight - 1) + shift])

        print("Returned from launch")

    # Decbounce button
    if button_pin.value() == True and button_down:
        button_down = False


# def menuTest():
#     while True:
#         if settings.BTN_ENC.value() == 0:
#
#             print("tlacitko zmacnuto")
#             while settings.BTN_ENC.value() == 0:
#                 continue
#
#
#         else:
#
#             print("tlacitko vypnuto")
#             while settings.BTN_ENC.value() == 1:
#                 continue
#
# menuTest()






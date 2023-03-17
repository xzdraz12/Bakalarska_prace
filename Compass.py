import math

import utime
from ustruct import pack
from array import array

import GPS
import settings

__gain__ = {
    '0.88': (0 << 5, 0.73),
    '1.3': (1 << 5, 0.92),
    '1.9': (2 << 5, 1.22),
    '2.5': (3 << 5, 1.52),
    '4.0': (4 << 5, 2.27),
    '4.7': (5 << 5, 2.56),
    '5.6': (6 << 5, 3.03),
    '8.1': (7 << 5, 4.35)
}

# Correction to be set after calibration
global xs, ys, xb, yb
xs = 1
ys = 0.8374885
xb = -261.69
yb = 370.27


def Calibration():
    settings.lcd.putstr("Provedte kalibraci kompasu")
    utime.sleep(1)
    settings.lcd.clear()
    settings.lcd.putstr("jeho otacenim 360°")
    utime.sleep(1)
    settings.lcd.clear()
    settings.lcd.putstr("pote stiskni tlacitko")
    settings.lcd.blink_cursor_on()

    Xmin = 1000
    Xmax = -1000
    Ymin = 1000
    Ymax = -1000

    while True:
        utime.sleep(0.2)
        x, y, z = read()
        Xmin = min(x, Xmin)
        Xmax = max(x, Xmax)
        Ymin = min(y, Ymin)
        Ymax = max(y, Ymax)
        print(settings.buzola.format_result(x, y, z))
        print("Xmin=" + str(Xmin) + "; Xmax=" + str(Xmax) + "; Ymin=" + str(Ymin) + "; Ymax=" + str(Ymax))

        if settings.button.value() == 1:
            print()
            print('Got ctrl-c')

            xs = 1
            ys = (Xmax - Xmin) / (Ymax - Ymin)
            xb = xs * (1 / 2 * (Xmax - Xmin) - Xmax)
            yb = xs * (1 / 2 * (Ymax - Ymin) - Ymax)
            print("Calibration corrections:")
            print("xs=" + str(xs))
            print("xb=" + str(xb))
            print("ys=" + str(ys))
            print("yb=" + str(yb))

            settings.lcd.blink_cursor_off()
            settings.lcd.clear()
            settings.lcd.putstr("kalibrace dokoncena")
            utime.sleep(2)
            settings.lcd.clear()

            break


def InitializeCompass():
    # Initialize sensor.
    settings.buzola.start()

    #i2c = machine.SoftI2C(scl=machine.Pin(scl), sda=machine.Pin(sda), freq=15000)
    # Configuration register A:
    #   0bx11xxxxx  -> 8 samples averaged per measurement
    #   0bxxx100xx  -> 15 Hz, rate at which data is written to output registers
    #   0bxxxxxx00  -> Normal measurement mode
    settings.buzola.writeto_mem(0x1e, 0x00, pack('B', 0b111000))

    # Configuration register B:
    reg_value, gain = __gain__[settings.gauss]
    settings.buzola.writeto_mem(0x1e, 0x01, pack('B', reg_value))

    # Set mode register to continuous mode.
    settings.buzola.writeto_mem(0x1e, 0x02, pack('B', 0x00))
    settings.buzola.stop()

    # Convert declination (tuple of degrees and minutes) to radians.
    declination = (settings.declination[0] + settings.declination[1] / 60) * math.pi / 180

    # Reserve some memory for the raw xyz measurements.
    data = array('B', [0] * 6)


def read():
    data = ""
    gain = ""


    buff = bytearray(255)
    buff = str(settings.buzola.readline())
    #buff = str(settings.buzola.readfrom_mem_into(0x1e, 0x03, data))
    #settings.buzola.readfrom_mem_into(0x1e, 0x03, data)

    x = (buff[0] << 8) | buff[1]
    y = (buff[4] << 8) | buff[5]
    z = (buff[2] << 8) | buff[3]

    x = x - (1 << 16) if x & (1 << 15) else x
    y = y - (1 << 16) if y & (1 << 15) else y
    z = z - (1 << 16) if z & (1 << 15) else z

    x = x * gain
    y = y * gain
    z = z * gain

    # Apply calibration corrections
    x = x * xs + xb
    y = y * ys + yb

    return x, y, z


def heading(x, y):
    heading_rad = math.atan2(y, x)
    heading_rad += settings.declination

    # Correct reverse heading.
    if heading_rad < 0:
        heading_rad += 2 * math.pi

    # Compensate for wrapping.
    elif heading_rad > 2 * math.pi:
        heading_rad -= 2 * math.pi

    # Convert from radians to degrees.
    heading = heading_rad * 180 / math.pi
    degrees = math.floor(heading)
    minutes = round((heading - degrees) * 60)
    return degrees, minutes


def format_result(x, y, z):
    degrees, minutes = heading(x, y)
    return 'X: {:.4f}, Y: {:.4f}, Z: {:.4f}, Heading: {}° {}′ '.format(x, y, z, degrees, minutes)


def GetCompassApi():
    import json
    import requests

    headers = {"API-Key": "<add_your_key>"}

    hostname = "https://geomag.amentum.io/wmm/magnetic_field"

    params = dict(
        altitude=10,  # [km]
        longitude=GPS.longitude,  # [deg]
        latitude=GPS.latitude,
        year=utime.gmtime()[0]+utime.gmtime()[1]/12  # decimal year, half-way through 2020
    )

    try:
        response = requests.get(hostname, params=params, headers=headers)
        # extract JSON payload of response as Python dictionary
        json_payload = response.json()
        # raise an Exception if we encoutnered any HTTP error codes like 404
        response.raise_for_status()
    except requests.exceptions.ConnectionError as e:
        # handle any typo errors in url or endpoint, or just patchy internet connection
        print(e)
    except requests.exceptions.HTTPError as e:
        # handle HTTP error codes in the response
        print(e, json_payload['error'])
    except requests.exceptions.RequestException as e:
        # general error handling
        print(e, json_payload['error'])
    else:
        json_payload = response.json()
        print(json.dumps(json_payload, indent=4, sort_keys=True))

#
#
# from machine import I2C
# import math
# from array import array
#
#
# class HMC5883L():
#     __scales = {
#         "0.88": [0, 0.73],
#         "1.3": [1, 0.92],
#         "1.9": [2, 1.22],
#         "2.5": [3, 1.52],
#         "4.0": [4, 2.27],
#         "4.7": [5, 2.56],
#         "5.6": [6, 3.03],
#         "8.1": [7, 4.35]}
#
#     def __init__(self, port=2, address=30, gauss="1.3", declination=(5, 65)):
#         self.bus = I2C(port, I2C.MASTER, baudrate=100000)
#         self.address = address
#         degrees, minutes = declination
#         self.__declDegrees = degrees
#         self.__declMinutes = minutes
#         self.__declination = (degrees + minutes / 60) * math.pi / 180
#         reg, self.__scale = self.__scales[gauss]
#         self.bus.mem_write(0x70, self.address, 0x00)  # 8 Average, 15 Hz, normal measurement
#         self.bus.mem_write(reg << 5, self.address, 0x01)  # Scale
#         self.bus.mem_write(0x00, self.address, 0x02)  # Continuous measurement
#
#     def declination(self):
#         return (self.__declDegrees, self.__declMinutes)
#
#     def twos_complement(self, val, len):  # Convert two's complement to integer
#         if (val & (1 << len - 1)):
#             val = val - (1 << len)
#         return val
#
#     def __convert(self, data, offset):
#         val = self.twos_complement(data[offset] << 8 | data[offset + 1], 16)
#         if val == -4096: return None
#         return round(val * self.__scale, 4)
#
#     def axes(self):
#         data = array('B', [0] * 6)
#         self.bus.mem_read(data, self.address,
#                           0x03)  # Reading just the necessary registers instead of the whole memory as it was in rm-hull's version
#         x = self.__convert(data, 0)
#         y = self.__convert(data, 4)
#         z = self.__convert(data, 2)
#         return (x, y, z)
#
#     def heading(self):
#         (x, y, z) = self.axes()
#         headingRad = math.atan2(y, x)
#         headingRad += self.__declination
#         # Correct for reversed heading
#         if headingRad < 0:
#             headingRad += 2 * math.pi
#         # Check for wrap and compensate
#         elif headingRad > 2 * math.pi:
#             headingRad -= 2 * math.pi
#         # Convert to degrees from radians
#         headingDeg = headingRad * 180 / math.pi
#         return headingDeg
#
#     def degrees(self, headingDeg):
#         degrees = math.floor(headingDeg)
#         minutes = round((headingDeg - degrees) * 60)
#         return (degrees, minutes)
#
#     def __str__(self):
#         (x, y, z) = self.axes()
#         return "Axis X: " + str(x) + "\n" \
#                                      "Axis Y: " + str(y) + "\n" \
#                                                            "Axis Z: " + str(z) + "\n" \
#                                                                                  "Heading: " + str(
#             self.heading()) + "\n"
#
# # "Declination: " + self.degrees(self.declination()) + "\n" \ #It gives an error on MicroPython and I've yet to see how it's supposed to work at all

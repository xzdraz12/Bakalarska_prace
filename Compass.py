
import math
import machine

from ustruct import pack
from array import array
import ujson
import urequests
import math
import machine

from ustruct import pack
from array import array

import CompassCalibration

import machine
from machine import I2C

import settings
import utime
import Compass

global declination, inclination
def GetCompassApi():


    altitude = "10"
    longitude = "49.3125"
    latitude = "17.3750"
    year = str(utime.gmtime()[0]+utime.gmtime()[1]/12)

    headers = {"API-Key": "VNFndFbOqgZ180EAPErDyCG5YQPBf3fY"}

    hostname = "https://geomag.amentum.io/wmm/magnetic_field?altitude="+altitude+"&longitude="+longitude+"&latitude="+longitude+"&year="+year


    response = urequests.request(method = "GET", url = hostname, data=None, json = None, headers=headers).text
    #print(response)
    json_payload = ujson.loads(response)

    declination = float(ujson.dumps(json_payload["declination"]["value"]))
    #print(declination)
    inclination = float(ujson.dumps(json_payload["inclination"]["value"]))
    #print(inclination)



global xs, ys, xb, yb
xs = ""
ys = ""
xb = ""
yb = ""


def Calibrate():


    sensor = Compass.HMC5883L()
    Xmin = 1000
    Xmax = -1000
    Ymin = 1000
    Ymax = -1000

    steps = 0
    num_of_steps = (720 / (360 / 200)) * 8

    part_full = num_of_steps - ((180 / (360 / 200)) * 8)  # plna rychlost, odcitam 180 protoze z obou stran 90
    parts_change = (num_of_steps - part_full) / 2

    delay_max = 0.007
    delay_min = 0.001

    speedup = (delay_max - delay_min) / (parts_change)
    print(speedup)

    settings.dir_az.value(0)
    for i in range(parts_change):
        settings.step_az.value(1)
        utime.sleep(delay_max - (i * speedup))
        settings.step_az.value(0)
        utime.sleep(delay_max - (i * speedup))
        x, y, z = sensor.read()
        Xmin = min(x, Xmin)
        Xmax = max(x, Xmax)
        Ymin = min(y, Ymin)
        Ymax = max(y, Ymax)

    for i in range(part_full):
        settings.step_az.value(1)
        utime.sleep(delay_min)
        settings.step_az.value(0)
        utime.sleep(delay_min)
        x, y, z = sensor.read()
        Xmin = min(x, Xmin)
        Xmax = max(x, Xmax)
        Ymin = min(y, Ymin)
        Ymax = max(y, Ymax)

    for i in range(parts_change):
        settings.step_az.value(1)
        utime.sleep(delay_min + (i * speedup))
        settings.step_az.value(0)
        utime.sleep(delay_min + (i * speedup))
        x, y, z = sensor.read()
        Xmin = min(x, Xmin)
        Xmax = max(x, Xmax)
        Ymin = min(y, Ymin)
        Ymax = max(y, Ymax)

    xs = 1
    ys = (Xmax - Xmin) / (Ymax - Ymin)
    xb = xs * (1 / 2 * (Xmax - Xmin) - Xmax)
    yb = xs * (1 / 2 * (Ymax - Ymin) - Ymax)
    #
    # print("Calibration corrections:")
    # print("xs=" + str(xs))
    # print("xb=" + str(xb))
    # print("ys=" + str(ys))
    # print("yb=" + str(yb))
    #
    # print(sensor.format_result(x, y, z))
    # print("Xmin=" + str(Xmin) + "; Xmax=" + str(Xmax) + "; Ymin=" + str(Ymin) + "; Ymax=" + str(Ymax))





#Calibrate()

class HMC5883L:
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

    # xs = CompassCalibration.xs
    # ys = CompassCalibration.ys
    # xb = CompassCalibration.xb
    # yb = CompassCalibration.yb




    def __init__(self, scl=3, sda=2, address=0x1e, gauss='1.9', declination=(Compass.declination, Compass.inclination)):
        self.i2c = i2c = machine.SoftI2C(scl=machine.Pin(scl), sda=machine.Pin(sda), freq=15000)

        # Initialize sensor.
        print("achoj"+str(self.xs))


        i2c.start()

        # Configuration register A:
        #   0bx11xxxxx  -> 8 samples averaged per measurement
        #   0bxxx100xx  -> 15 Hz, rate at which data is written to output registers
        #   0bxxxxxx00  -> Normal measurement mode
        i2c.writeto_mem(0x1e, 0x00, pack('B', 0b111000))

        # Configuration register B:
        reg_value, self.gain = self.__gain__[gauss]
        i2c.writeto_mem(0x1e, 0x01, pack('B', reg_value))

        # Set mode register to continuous mode.
        i2c.writeto_mem(0x1e, 0x02, pack('B', 0x00))
        i2c.stop()

        # Convert declination (tuple of degrees and minutes) to radians.
        self.declination = (declination[0] + declination[1] / 60) * math.pi / 180

        # Reserve some memory for the raw xyz measurements.
        self.data = array('B', [0] * 6)

    def read(self):
        data = self.data
        gain = self.gain

        self.i2c.readfrom_mem_into(0x1e, 0x03, data)

        x = (data[0] << 8) | data[1]
        y = (data[4] << 8) | data[5]
        z = (data[2] << 8) | data[3]

        x = x - (1 << 16) if x & (1 << 15) else x
        y = y - (1 << 16) if y & (1 << 15) else y
        z = z - (1 << 16) if z & (1 << 15) else z

        x = x * gain
        y = y * gain
        z = z * gain

        # Apply calibration corrections
        x = x * self.xs + self.xb
        y = y * self.ys + self.yb

        return x, y, z

    def heading(self, x, y):
        heading_rad = math.atan2(y, x)
        heading_rad += self.declination



        # Correct reverse heading.
        if heading_rad < 0:
            heading_rad += 2 * math.pi

        # Compensate for wrapping.
        elif heading_rad > 2 * math.pi:
            heading_rad -= 2 * math.pi

        # Convert from radians to degrees.
        heading = heading_rad * 180 / math.pi
        print(heading_rad)
        degrees = math.floor(heading)
        minutes = round((heading - degrees) * 60)
        return degrees, minutes

    def format_result(self, x, y, z):
        degrees, minutes = self.heading(x, y)
        return 'X: {:.4f}, Y: {:.4f}, Z: {:.4f}, Heading: {}° {}′ '.format(x, y, z, degrees, minutes)



machine.freq(240000000)
GetCompassApi()
Calibrate()
sensor = Compass.HMC5883L()

while True:
    utime.sleep(1)
    x, y, z = sensor.read()
    print(sensor.format_result(x, y, z))
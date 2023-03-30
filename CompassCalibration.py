import ujson
import urequests
import utime
import machine

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




machine.freq(240000000)
GetCompassApi()

sensor = Compass.HMC5883L()

while True:
    utime.sleep(1)
    x, y, z = sensor.read()
    print(sensor.format_result(x, y, z))

#Calibrate()



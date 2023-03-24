from machine import I2C
from Compass import HMC5883L

import GPS
import utime
import Motors
import ujson
import urequests



def Calibrate():
    sensor = HMC5883L()

    Xmin = 1000
    Xmax = -1000
    Ymin = 1000
    Ymax = -1000

    while True:
        utime.sleep(0.2)
        x, y, z = sensor.read()
        Xmin = min(x, Xmin)
        Xmax = max(x, Xmax)
        Ymin = min(y, Ymin)
        Ymax = max(y, Ymax)

        steps = 1

        pins = Motors.pins_elevation
        for x in range(steps):
            for step in Motors.full_step_forward:
                for i in range(len(pins)):
                    pins[i].value(step[i])
                    utime.sleep(0.001)
                    x = x + 1

        if x == 13536:
            Motors.DeactivateStepper("azimuth")

            xs = 1
            ys = (Xmax - Xmin) / (Ymax - Ymin)
            xb = xs * (1 / 2 * (Xmax - Xmin) - Xmax)
            yb = xs * (1 / 2 * (Ymax - Ymin) - Ymax)
            print("Calibration corrections:")
            print("xs=" + str(xs))
            print("xb=" + str(xb))
            print("ys=" + str(ys))
            print("yb=" + str(yb))

            print(sensor.format_result(x, y, z))
            print("Xmin=" + str(Xmin) + "; Xmax=" + str(Xmax) + "; Ymin=" + str(Ymin) + "; Ymax=" + str(Ymax))
            break


        #except KeyboardInterrupt:





# def MyGetCompassApi():
#     headers = {"API-Key": "<VNFndFbOqgZ180EAPErDyCG5YQPBf3fY>"}
#
#     # longitude = "49.3125"  # [deg]
#     # latitude= "17.3750"
#     # altitude = "0"
#
#     # url = "https://geomag.amentum.io/wmm/magnetic_field"
#
#     # params = dict(
#     #     altitude=0,  # [km]
#     #     longitude=49.3125,  # [deg]
#     #     latitude=17.3750,
#     #     year=utime.gmtime()[0] + utime.gmtime()[1] / 12  # decimal year, half-way through 2020
#     # )
#
#     params = {
#         altitude=0,  # [km]
#         longitude=49.3125,  # [deg]
#         latitude=17.3750,
#         year=utime.gmtime()[0] + utime.gmtime()[1] / 12 # decimal year, half-way through 2020
#     }
#
#     year = str(utime.gmtime()[0] + utime.gmtime()[1] / 12)
#
#     # url = "https://geomag.amentum.io/wmm/magnetic_field?altitude=" + altitude + "&latitude="+latitude+"&longitude="+longitude+"&year="+year
#     # print(url)
#     url = "https://geomag.amentum.io/wmm/magnetic_field"
#     GetDeclination = urequests.get(url=url, data=params, json=None, headers=headers)
#
#     GetDeclination_json = GetDeclination.json()
#
#     print(GetDeclination_json)


# def GetCompassApi():
#
#     headers = {"API-Key": "<VNFndFbOqgZ180EAPErDyCG5YQPBf3fY>"}
#
#     hostname = "https://geomag.amentum.io/wmm/magnetic_field"
#
#     params = dict(
#         altitude=10,  # [km]
#         longitude=GPS.longitude,  # [deg]
#         latitude=GPS.latitude,
#         year=utime.gmtime()[0]+utime.gmtime()[1]/12  # decimal year, half-way through 2020
#     )
#
#     try:
#         response = urequests.get(hostname, params=params, headers=headers)
#         json_payload = response.json()
#         response.raise_for_status()
#     except urequests.exceptions.ConnectionError as e:
#         print(e)
#
#     except urequests.exceptions.HTTPError as e:
#         print(e, json_payload['error'])
#
#     except urequests.exceptions.RequestException as e:
#         print(e, json_payload['error'])
#
#     else:
#         json_payload = response.json()
#         print(ujson.dumps(json_payload, indent=4, sort_keys=True))
#

Calibrate()

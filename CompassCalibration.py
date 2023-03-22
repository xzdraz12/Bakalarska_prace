
from machine import I2C
from Compass import HMC5883L
from time import sleep
import GPS
import utime


def Calibrate():
    sensor = HMC5883L()

    Xmin = 1000
    Xmax = -1000
    Ymin = 1000
    Ymax = -1000

    while True:
        try:
            sleep(0.2)
            x, y, z = sensor.read()
            Xmin = min(x, Xmin)
            Xmax = max(x, Xmax)
            Ymin = min(y, Ymin)
            Ymax = max(y, Ymax)
            print(sensor.format_result(x, y, z))
            print("Xmin=" + str(Xmin) + "; Xmax=" + str(Xmax) + "; Ymin=" + str(Ymin) + "; Ymax=" + str(Ymax))

        except KeyboardInterrupt:
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
            break



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
import machine
import time
import math

import settings

# Define I2C bus pins
i2c = machine.I2C(1, scl=machine.Pin(1), sda=machine.Pin(0))

# Define HMC5883L address
HMC5883L_ADDR = 0x1e

# Define calibration variables
offsets = [0, 0, 0]
scale = [1, 1, 1]


# Initialize magnetometer
def init():
    global offsets, scale

    # Set HMC5883L to continuous mode
    i2c.writeto_mem(HMC5883L_ADDR, 0x02, b'\x00')

    # Collect data for automatic calibration
    data = []
    for i in range(1000):
        i2c.writeto_mem(HMC5883L_ADDR, 0x00, b'\x03')
        time.sleep(0.01)
        raw_data = i2c.readfrom_mem(HMC5883L_ADDR, 0x03, 6)
        x = (raw_data[0] << 8) | raw_data[1]
        y = (raw_data[4] << 8) | raw_data[5]
        z = (raw_data[2] << 8) | raw_data[3]
        data.append([x, y, z])

    # Calculate offsets
    for i in range(3):
        total = 0
        for j in range(1000):
            total += data[j][i]
        offsets[i] = total / 1000

    # Calculate scale factors
    x_range = max([abs(row[0] - offsets[0]) for row in data])
    y_range = max([abs(row[1] - offsets[1]) for row in data])
    z_range = max([abs(row[2] - offsets[2]) for row in data])
    scale[0] = x_range / 1000 if x_range != 0 else 1
    scale[1] = y_range / 1000 if y_range != 0 else 1
    scale[2] = z_range / 1000 if z_range != 0 else 1


# Read magnetometer data
def read():
    i2c.writeto_mem(HMC5883L_ADDR, 0x00, b'\x03')
    time.sleep(0.01)
    raw_data = i2c.readfrom_mem(HMC5883L_ADDR, 0x03, 6)
    x = (raw_data[0] << 8) | raw_data[1]
    y = (raw_data[4] << 8) | raw_data[5]
    z = (raw_data[2] << 8) | raw_data[3]
    x = (x - offsets[0]) / scale[0]
    y = (y - offsets[1]) / scale[1]
    z = (z- offsets[2]) / scale[2]
    return [x, y, z]


# Calculate heading in degrees
def heading(x, y):
    heading = math.atan2(y, x)
    if heading < 0:
        heading += 2 * math.pi
    return heading * 180 / math.pi


# Initialize magnetometer and start loop
# init()
# while True:
#     x, y, z = read()
#     print("X: {:.2f} Y: {:.2f} Z: {:.2f}".format(x, y, z))
#     print("Heading: {:.2f} degrees".format(heading(x, y)))
#     time.sleep(0.5)


# Initialize magnetometer and start loop
init()
while True:
    x, y, z = read()
    print("Raw X: {} Raw Y: {}".format(x, y))
    print("Scaled X: {:.2f} Scaled Y: {:.2f} Scaled Z: {:.2f}".format(x, y, z))
    print("Heading: {:.2f} degrees".format(heading(x, y)))
    settings.lcd.putstr("Heading: {:.2f} degrees".format(heading(x, y)))
    time.sleep(0.5)

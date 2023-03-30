import time

from machine import RTC
import utime
#nastaveni i2c pro displej

from pico_i2c_lcd import I2cLcd
from machine import I2C, UART, Pin
import machine

#
#nastaveni displeje
global I2C_ADDR,I2C_NUM_ROWS,I2C_NUM_COLS,lcd

I2C_ADDR = 0x20
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

Display_i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(Display_i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)


#nastaveni testovaciho tlacitka
led = machine.Pin(25, machine.Pin.OUT)
button = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_DOWN)


# # #nastaveni kompasu
# from Compass import HMC5883L
# global buzola,declination
# #buzola = machine.I2C(1, scl=machine.Pin(3), sda=machine.Pin(2), freq=15000)
# buzola = HMC5883L(scl=3, sda=2)
# gauss='1.9'
# declination=(0, 0)


#nastaveni casu
global timezone
global DaylightSaving

DaylightSaving = 1 #  pro letni cas, 0 pro zimni
timezone = 1


#krokove motory
#azimut
steps_per_revolution_azim = 200
step_az = Pin(28, Pin.OUT)
dir_az = Pin(27, Pin.OUT)






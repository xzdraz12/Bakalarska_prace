import time

from machine import RTC
import utime
#nastaveni i2c pro displej

from pico_i2c_lcd import I2cLcd
from machine import I2C, UART, Pin
import machine


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


#nastaveni kompasu
global buzola,declination
buzola = machine.I2C(1, scl=machine.Pin(3), sda=machine.Pin(2), freq=15000)
gauss='1.9'
declination=(0, 0)


#nastaveni casu
import ntptime

global timezone
global DaylightSaving


DaylightSaving = False
timezone = 3
ntpserver = "195.113.144.201"
def Get_Local_NTP_time():
    ntptime.settime()
    print(time.localtime())
    print(time.time())



Get_Local_NTP_time()





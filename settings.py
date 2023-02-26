
#nastaveni i2c pro displej

from pico_i2c_lcd import I2cLcd
from machine import I2C, UART, Pin
import machine
import settings

global I2C_ADDR,I2C_NUM_ROWS,I2C_NUM_COLS,lcd,i2c

I2C_ADDR = 0x20
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, settings.I2C_ADDR, settings.I2C_NUM_ROWS, settings.I2C_NUM_COLS)


#nastaveni testovaciho tlacitka
led = machine.Pin(25, machine.Pin.OUT)
button = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_DOWN)






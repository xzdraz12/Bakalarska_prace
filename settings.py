#nastaveni i2c pro displej
from machine import I2C, Pin
from ssd1306 import SSD1306_I2C

WIDTH = 128
HEIGHT = 64
i2c = I2C(1, scl = Pin(7), sda = Pin(6), freq=200000)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)




#enkoder
BTN_ENC = Pin(11, Pin.IN, Pin.PULL_UP)
BTN_EN1 = Pin(10, Pin.IN, Pin.PULL_UP)
BTN_EN2 = Pin(9, Pin.IN, Pin.PULL_UP)


#listy se satelity
RadioSatellites =["14781", "53385","43678","53385","25544","51085", "49396"]
WeatherSatellites = ["14781"]
ISS = ["1222"]






#nastaveni testovaciho tlacitka
#led = machine.Pin(25, machine.Pin.OUT)
#button = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_DOWN)


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
step_az = Pin(16, Pin.OUT)
dir_az = Pin(17, Pin.OUT)

#elevace
steps_per_revolution_elev = 200
step_el = Pin(18, Pin.OUT)
dir_el = Pin(19, Pin.OUT)

#Vyhledavani preletu
licenseKey = "TLX2JG-94DFXJ-K57JEF-4XB1"
MinElevation = "0"
DaysPrediction = "2"
ObserverAltitude = "0"






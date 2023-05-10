# import machine
# from machine import Pin, I2C
# from ssd1306 import SSD1306_I2C
# import framebuf
#
# WIDTH = 128
# HEIGHT = 32
#
# i2c = I2C(1, scl = machine.Pin(7), sda = machine.Pin(6), freq=200000)
#
#
# oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
#
# oled.text("hello world", 5,8)
# oled.show()
# print("provedeno")


from machine import Pin, I2C
scl  = Pin(7)
sda = Pin(6)

i2c = I2C(1, scl=scl, sda=sda, freq=200000)

address = i2c.scan()
print(address)

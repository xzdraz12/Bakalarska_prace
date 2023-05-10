# import UART
from machine import UART
# import GPIO
from machine import Pin
# import ADC
from machine import ADC
# import time for delay
import time
# import thread for multicore support
import _thread
# import machine to overlock board
import machine

# init uart 0 with specified pins
# uart0 = UART(0, baudrate=921600, tx=Pin(16), rx=Pin(17), timeout=10, timeout_char=1)
uart0 = UART(1, baudrate=1500000, tx=Pin(16), rx=Pin(17))

# create ADC object on ADC pin, GP29 is connected do VSYS on Pico
adc = ADC(Pin(29))
adc_temp = ADC(4)
test_sig = ADC(Pin(28))

power_meas_voltage = ADC(Pin(26))
power_meas_current = ADC(Pin(27))

# init build-in LED
LED = Pin(25, Pin.OUT)

# pin to enable/disable measurement
# LOW - not measuring, HIGH - measuring data and sending to console
MEASUREMENT_ENABLE_PIN = Pin(22, Pin.IN, Pin.PULL_DOWN)

# measurement enable LED
MEASUREMENT_ON_LED = Pin(20, Pin.OUT)

# dedicated button for user input actions
USER_BUTTON = Pin(21, Pin.IN, Pin.PULL_DOWN)

# enable flag to trigger Autoranging mode
# currently only mA and uA range supported
AUTORANGING = False

# information about last measurement range
# 0 - mA, 1 -uA
measuring_range = 0

# global variables
# internal temperature of MCU
internal_temperature_celsius = 0


# app thread for core 1
# mainly used for reading voltage and current value from power source to log data
def thread_core1():
    global internal_temperature_celsius
    global measuring_range

    # measured variable applied for current thread only
    voltage = 0
    current = 0
    internal_temperature_adc = 0

    # time storage variables
    lastTime = 0
    deltaTime = 0

    # status information and buffer for current, voltage measurement
    dataCounter = 0
    sampleCount = 10
    outBuffer = [0] * sampleCount * 4

    # fill in buffer with zeroes
    for i in range(sampleCount):
        outBuffer[i] = 0

    MEASUREMENT_ON_LED.off()

    lastTime = time.ticks_us()

    while (1):
        # delta time in us
        deltaTime = time.ticks_diff(time.ticks_us(), lastTime)

        # check if difference in last measurement is higher, then take new measurement
        if (deltaTime >= 250):

            # check measurement enable
            if 1 == 1:
                # if(MEASUREMENT_ENABLE_PIN.value() == 1):

                # measurement optical indication
                MEASUREMENT_ON_LED.on()
                MEASUREMENT_ON_LED.off()

                # voltage and current reading
                voltage = power_meas_voltage.read_u16()
                current = power_meas_current.read_u16()

                # save of last measurement
                lastTime = time.ticks_us()

                # check autoranging and if so, automatically change range
                if (AUTORANGING):
                    # switch from mA to uA range
                    if (current >= 48000 and measuring_range == 0):
                        measuring_range = 1
                    # switch from uA range to mA
                    elif (current <= 8000 and measuring_range == 1):
                        measuring_range = 0

                # format voltage and current reading into byte format in output buffer
                outBuffer[dataCounter] = (voltage >> 8) & 0xFF
                outBuffer[dataCounter + 1] = (voltage) & 0xFF
                outBuffer[dataCounter + 2] = (current >> 8) & 0xFF
                outBuffer[dataCounter + 3] = (current) & 0xFF

                # check if output buffer is filled, then send it all over UART to USB to PC
                if (dataCounter >= ((sampleCount - 1) * 4)):
                    byteArr = bytearray(outBuffer)
                    uart0.write(byteArr)
                    dataCounter = 0
                else:
                    dataCounter = dataCounter + 4

            # measurement not enabled
            else:
                MEASUREMENT_ON_LED.off()

            # internal temperature measurement
            internal_temperature_adc = (adc_temp.read_u16() / 0xFFFF) * 3300
            internal_temperature_celsius = 27 - (internal_temperature_adc - 0.706) * 0.001721

        # reduce check interval to 1 us so it wont overload core
        time.sleep_us(1)


# app thread for core 0
def thread_core0():
    global internal_temperature_celsius
    global measuring_range
    global AUTORANGING

    counter_main = 0
    user_input_state = 0
    AUTORANGING = False

    while (1):
        counter_main = counter_main + 1

        user_input_state = USER_BUTTON.value()

        LED.value(counter_main % 2)

        print("Running counter: " + str(counter_main))
        print("Temp " + str(internal_temperature_celsius) + "°C")
        print("User input: " + str(user_input_state))
        print("Autoranging: " + str(AUTORANGING) + ", Measuring range: " + str(measuring_range))

        time.sleep_ms(500)


########################################################################
##### START OF THE CODE ################################################
########################################################################

# first overclock CPU to max. speed
print("Core freq: " + str(machine.freq() / 1000000) + "MHz")
# OC to 240 MHz
machine.freq(240000000)
time.sleep_ms(250)
print("Core freq: " + str(machine.freq() / 1000000) + "MHz")

# start thread on core 1
_thread.start_new_thread(thread_core1, ())

# by default core 0 is occupied by default code
thread_core0()



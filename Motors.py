from machine import Pin
import utime

import settings




global pins_elevation, pins_azim, full_step_forward, full_step_backward
pins_elevation = [
    Pin(21, Pin.OUT),
    Pin(20, Pin.OUT),
    Pin(19, Pin.OUT),
    Pin(18, Pin.OUT)
]



full_step_forward = [
    [1,0,0,0],
    [0,1,0,0],
    [0,0,1,0],
    [0,0,0,1]

]

full_step_backward = [
    [0,0,0,1],
    [0,0,1,0],
    [0,1,0,0],
    [1,0,0,0]
]

# azimutalni osa
steps_per_revolution_azim = 200
step = Pin(28, Pin.OUT)
dir = Pin(27, Pin.OUT)

def rotate_azimuth_slew(angle, direction, microstep):
    #num_of_steps = map(angle,0,360,0,400)
    num_of_steps = (angle/(360/200))*microstep
    if direction == "cw":
        dir.value(0)
        for i in range(num_of_steps):
            step.value(1)
            utime.sleep(.002)
            step.value(0)
            utime.sleep(.002)

    if direction == "ccw":
        dir.value(1)
        for i in range(num_of_steps):
            step.value(0)
            utime.sleep(.002)
            step.value(1)
            utime.sleep(.002)


def rotate_azimuth_change_speed(angle, direction, microstep):
    num_of_steps = ((angle/2)/(360/200))*microstep

    delay_max = 0.007
    delay_min = 0.002

    speedup = (delay_max-delay_min)/(num_of_steps)
    if direction == "cw":
        dir.value(0)
        for i in range(num_of_steps):
            step.value(1)
            utime.sleep(delay_max-(i*speedup))
            step.value(0)
            utime.sleep(delay_max-(i*speedup))
            print(speedup)

        for i in range(num_of_steps):
            step.value(1)
            utime.sleep(delay_min+(i*speedup))
            step.value(0)
            utime.sleep(delay_min+(i*speedup))

    if direction == "ccw":
        dir.value(1)
        for i in range(num_of_steps):
            step.value(1)
            utime.sleep(delay_max - (i * speedup))
            step.value(0)
            utime.sleep(delay_max - (i * speedup))
            print(speedup)

        for i in range(num_of_steps):
            step.value(1)
            utime.sleep(delay_min + (i * speedup))
            step.value(0)
            utime.sleep(delay_min + (i * speedup))





#elevacni osa
def move_stepper(angle, direction, type):
    steps_to_one_degree = 512/360
    steps = angle*steps_to_one_degree
    if type == "azimuth":
        pins = pins_azim

        if direction == "clockwise":
            for x in range(steps):
                for step in full_step_forward:
                    for i in range(len(pins)):
                        pins[i].value(step[i])
                        utime.sleep(0.001)
                        x = x + 1

        if direction == "counterclockwise":
            for x in range(steps):
                for step in full_step_backward:
                    for i in range(len(pins)):
                        pins[i].value(step[i])
                        utime.sleep(0.0009)
                        x = x + 1


    elif type == "elevation":
        pins = pins_elevation

        if direction == "clockwise":
            for x in range(steps):
                for step in full_step_forward:
                    for i in range(len(pins)):
                        pins[i].value(step[i])
                        utime.sleep(0.00009)
                        x = x + 1

        if direction == "counterclockwise":
            for x in range(steps):
                for step in full_step_backward:
                    for i in range(len(pins)):
                        pins[i].value(step[i])
                        utime.sleep(0.0009)
                        x = x + 1



def move_stepper_fast(angle, direction, type):
    steps_to_one_degree = 512 / 360
    steps = angle * steps_to_one_degree
    if type == "azimuth":
        pins = pins_azim
        for x in range(steps):
            for step in full_step_forward:
                for i in range(len(pins)):
                    pins[i].value(step[i])
                    utime.sleep(0.001)
                    x = x + 1

    elif type == "elevation":
        pins = pins_elevation
        for x in range(steps):
            for step in full_step_backward:
                for i in range(len(pins)):
                    pins[i].value(step[i])
                    utime.sleep(0.001)
                    x = x + 1


def DeactivateStepper(type):
    if type == "azimuth":
        pins = pins_azim
        for i in range(len(pins)):
            pins[i].value(0)

    elif type == "elevation":
        pins = pins_elevation
        for i in range(len(pins)):
            pins[i].value(0)


def CalibrateElevation():

    while True:
        while settings.button.value() == 0:
            steps = 1
            pins = pins_elevation
            for x in range(steps):
                for step in full_step_forward:
                    for i in range(len(pins)):
                        pins[i].value(step[i])
                        utime.sleep(0.001)
                        x = x + 1

        if settings.button.value() == 1:
            #DeactivateStepper("elevation")
            move_stepper(20, "counterclockwise", "elevation", 0.01)

            while settings.button.value() == 0:
                steps = 1
                pins = pins_elevation
                for x in range(steps):
                    for step in full_step_forward:
                        for i in range(len(pins)):
                            pins[i].value(step[i])
                            utime.sleep(0.01)
                            x = x + 1

            
            if settings.button.value() == 1:
                DeactivateStepper("elevation")
                break


#def CalibrateAzimuth():

#rotate_azimuth_slew(10, "ccw", 8)

#CalibrateElevation()
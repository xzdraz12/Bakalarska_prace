from machine import Pin
import utime

import menu
import settings

steps_per_revolution = 512

pins_elevation = [
    Pin(21, Pin.OUT),
    Pin(20, Pin.OUT),
    Pin(19, Pin.OUT),
    Pin(18, Pin.OUT)
]

pins_azim = ""

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


half_step_backward = [
    [0,0,1,1],
    [0,1,1,0],
    [1,1,0,0],
    [1,0,0,1]
]

quarter_step_backward = [
    [0,1,1,1],
    [1,1,1,0],
    [1,1,0,1],
    [1,0,1,1]
]



def move_stepper(angle, direction, type, speed):
    steps_to_one_degree = steps_per_revolution/360
    steps = angle*steps_to_one_degree
    if type == "azimuth":
        pins = pins_azim

        if direction == "clockwise":
            for x in range(steps):
                for step in full_step_forward:
                    for i in range(len(pins)):
                        pins[i].value(step[i])
                        utime.sleep(speed)
                        x = x + 1

        if direction == "counterclockwise":
            for x in range(steps):
                for step in full_step_backward:
                    for i in range(len(pins)):
                        pins[i].value(step[i])
                        utime.sleep(speed)
                        x = x + 1


    elif type == "elevation":
        pins = pins_elevation

        if direction == "clockwise":
            for x in range(steps):
                for step in full_step_forward:
                    for i in range(len(pins)):
                        pins[i].value(step[i])
                        utime.sleep(speed)
                        x = x + 1

        if direction == "counterclockwise":
            for x in range(steps):
                for step in full_step_backward:
                    for i in range(len(pins)):
                        pins[i].value(step[i])
                        utime.sleep(speed)
                        x = x + 1



def move_stepper_fast(angle, direction, type):
    steps_to_one_degree = steps_per_revolution / 360
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



CalibrateElevation()
from machine import Pin
import utime

steps_per_revolution = 512

pins = [
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



def move_stepper(angle, direction):
    steps_to_one_degree = steps_per_revolution/360
    print(steps_to_one_degree)
    steps = int(angle*steps_to_one_degree)
    print(steps)

    if direction == "clockwise":
        for x in range(steps):
            for step in full_step_forward:
                for i in range(len(pins)):
                    pins[i].value(step[i])
                    utime.sleep(0.001)
                    x = x + 1
    if direction == "anticlockwise":
        for x in range(steps):
            for step in full_step_backward:
                for i in range(len(pins)):
                    pins[i].value(step[i])
                    utime.sleep(0.001)
                    x = x + 1




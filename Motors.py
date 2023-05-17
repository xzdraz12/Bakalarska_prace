import utime

import settings

# azimutalni osa
steps_az = settings.steps_per_revolution_azim
steps_el = settings.steps_per_revolution_elev
def rotate_azimuth_slew(angle, direction, microstep):
    #num_of_steps = map(angle,0,360,0,400)
    num_of_steps = (angle/(360/steps_az))*microstep
    if direction == "cw":
        settings.dir_az.value(0)
        for i in range(num_of_steps):
            settings.step_az.value(1)
            utime.sleep(.002)
            settings.step_az.value(0)
            utime.sleep(.002)

    if direction == "ccw":
        settings.dir_az.value(1)
        for i in range(num_of_steps):
            settings.step_az.value(0)
            utime.sleep(.002)
            settings.step_az.value(1)
            utime.sleep(.002)


def rotate_azimuth_change_speed(angle, direction, microstep):
    delay_max = 0.009
    delay_min = 0.001


    if angle <= 180:
        num_of_steps = ((angle / (360 / steps_az)) * microstep)/2
        speedup = (delay_max - delay_min) / (num_of_steps)
        if direction == "cw":
            settings.dir_az.value(0)
            for i in range(num_of_steps):
                settings.step_az.value(1)
                utime.sleep(delay_max-(i*speedup))
                settings.step_az.value(0)
                utime.sleep(delay_max-(i*speedup))


            for i in range(num_of_steps):
                settings.step_az.value(1)
                utime.sleep(delay_min+(i*speedup))
                settings.step_az.value(0)
                utime.sleep(delay_min+(i*speedup))

        if direction == "ccw":
            settings.dir_az.value(1)
            for i in range(num_of_steps):
                settings.step_az.value(1)
                utime.sleep(delay_max - (i * speedup))
                settings.step_az.value(0)
                utime.sleep(delay_max - (i * speedup))


            for i in range(num_of_steps):
                settings.step_az.value(1)
                utime.sleep(delay_min + (i * speedup))
                settings.step_az.value(0)
                utime.sleep(delay_min + (i * speedup))

    else:
        num_of_steps = (angle / (360 / steps_az)) * microstep

        part_full = num_of_steps-((180/(360/steps_az))*microstep)
        parts_change = (num_of_steps-part_full)/2

        speedup = (delay_max - delay_min) / (parts_change)
        print(speedup)
        if direction == "cw":
            settings.dir_az.value(0)
            for i in range(parts_change):
                settings.step_az.value(1)
                utime.sleep(delay_max - (i * speedup))
                settings.step_az.value(0)
                utime.sleep(delay_max - (i * speedup))
                print(delay_max - (i * speedup))

            for i in range(part_full):
                settings.step_az.value(1)
                utime.sleep(delay_min)
                settings.step_az.value(0)
                utime.sleep(delay_min)
                #print(delay_min)

            for i in range(parts_change):
                settings.step_az.value(1)
                utime.sleep(delay_min + (i * speedup))
                settings.step_az.value(0)
                utime.sleep(delay_min + (i * speedup))


        if direction == "ccw":
            settings.dir_az.value(1)
            for i in range(parts_change):
                settings.step_az.value(1)
                utime.sleep(delay_max - (i * speedup))
                settings.step_az.value(0)
                utime.sleep(delay_max - (i * speedup))

            for i in range(part_full):
                settings.step_az.value(1)
                utime.sleep(delay_min)
                settings.step_az.value(0)
                utime.sleep(delay_min)

            for i in range(parts_change):
                settings.step_az.value(1)
                utime.sleep(delay_min + (i * speedup))
                settings.step_az.value(0)
                utime.sleep(delay_min + (i * speedup))

#elevační osa

def rotate_elevation_slew(angle, direction, microstep):
    #num_of_steps = map(angle,0,360,0,400)
    num_of_steps = (angle/(360/steps_el))*microstep
    if direction == "cw":
        settings.dir_el.value(0)
        for i in range(num_of_steps):
            settings.step_el.value(1)
            utime.sleep(.002)
            settings.step_el.value(0)
            utime.sleep(.002)

    if direction == "ccw":
        settings.dir_el.value(1)
        for i in range(num_of_steps):
            settings.step_el.value(0)
            utime.sleep(.002)
            settings.step_el.value(1)
            utime.sleep(.002)

def rotate_elevation_change_speed(angle, direction, microstep):
    delay_max = 0.009
    delay_min = 0.001

    if angle <= 180:
        num_of_steps = ((angle / (360 / steps_el)) * microstep) / 2
        speedup = (delay_max - delay_min) / (num_of_steps)
        if direction == "cw":
            settings.dir_el.value(0)
            for i in range(num_of_steps):
                settings.step_el.value(1)
                utime.sleep(delay_max - (i * speedup))
                settings.step_el.value(0)
                utime.sleep(delay_max - (i * speedup))

            for i in range(num_of_steps):
                settings.step_el.value(1)
                utime.sleep(delay_min + (i * speedup))
                settings.step_el.value(0)
                utime.sleep(delay_min + (i * speedup))

        if direction == "ccw":
            settings.dir_el.value(1)
            for i in range(num_of_steps):
                settings.step_el.value(1)
                utime.sleep(delay_max - (i * speedup))
                settings.step_el.value(0)
                utime.sleep(delay_max - (i * speedup))

            for i in range(num_of_steps):
                settings.step_el.value(1)
                utime.sleep(delay_min + (i * speedup))
                settings.step_el.value(0)
                utime.sleep(delay_min + (i * speedup))

    else:
        num_of_steps = (angle / (360 / steps_el)) * microstep

        part_full = num_of_steps - (
                    (180 / (360 / steps_el)) * microstep)  # plna rychlost, odcitam 180 protoze z obou stran 90
        parts_change = (num_of_steps - part_full) / 2

        speedup = (delay_max - delay_min) / (parts_change)
        print(speedup)
        if direction == "cw":
            settings.dir_el.value(0)
            for i in range(parts_change):
                settings.step_el.value(1)
                utime.sleep(delay_max - (i * speedup))
                settings.step_el.value(0)
                utime.sleep(delay_max - (i * speedup))
                print(delay_max - (i * speedup))

            for i in range(part_full):
                settings.step_el.value(1)
                utime.sleep(delay_min)
                settings.step_el.value(0)
                utime.sleep(delay_min)
                # print(delay_min)

            for i in range(parts_change):
                settings.step_el.value(1)
                utime.sleep(delay_min + (i * speedup))
                settings.step_el.value(0)
                utime.sleep(delay_min + (i * speedup))

        if direction == "ccw":
            settings.dir_el.value(1)
            for i in range(parts_change):
                settings.step_el.value(1)
                utime.sleep(delay_max - (i * speedup))
                settings.step_el.value(0)
                utime.sleep(delay_max - (i * speedup))

            for i in range(part_full):
                settings.step_el.value(1)
                utime.sleep(delay_min)
                settings.step_el.value(0)
                utime.sleep(delay_min)

            for i in range(parts_change):
                settings.step_el.value(1)
                utime.sleep(delay_min + (i * speedup))
                settings.step_el.value(0)
                utime.sleep(delay_min + (i * speedup))


#def CalibrateAzimuth():

rotate_azimuth_change_speed(360, "cw", 1)

#CalibrateElevation()
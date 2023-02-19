import machine
import utime
import menu
import settings

def clear():
    settings.lcd.clear()
    

menu.welcome()

utime.sleep(3)

menu.GettingGPS()

utime.sleep(3)


    
while True:
    

    if settings.button.value()==1:
        clear()
        settings.led.value(1)
        settings.lcd.putstr("Tlacitko zmacknuto")
        while settings.button.value()==1:
            continue
            
        
    else:
        clear()
        settings.led.value(0)
        settings.lcd.putstr("Tlacitko pusteno")
        while settings.button.value()==0:
            continue
        
        
    







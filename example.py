#! /usr/bin/python2

import time
import sys
from firebase import firebase

EMULATE_HX711=False

# referce unit would be changed while load cell testing 
referenceUnit = 1

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
        
    print("Bye!")
    sys.exit()
	

#this values are corresponding to gpio pins which connected to clk and dat inputs in hx711 amplifier.

hx = HX711(17, 4)



hx.set_reading_format("MSB", "MSB")

# HOW TO CALCULATE THE REFFERENCE UNIT
# To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
# In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
# and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
# If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.

#hx.set_reference_unit(113)
hx.set_reference_unit(referenceUnit)

hx.reset()

hx.tare()

firebase = firebase.FirebaseApplication('https://raspberrypi-1443d.firebaseio.com/', None)

def updateDatabase():

        val = hx.get_weight(5)

        print("Tare done! Add weight now...")
        
		sleep(5)
		print(val)
         
		hx.power_down()
        hx.power_up()
		
		data = {"weight": val}
	    firebase.post('/sensor/dht', data)


while True:
    try:
	     updateDabase()
        
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
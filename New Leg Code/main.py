from dogLeg import *
from jointControl2 import *
from secrets import tufts_eecs as connection
import machine
import sys
name = "backLeft"

stopPin = machine.Pin(25, machine.Pin.IN, machine.Pin.PULL_UP)
led = machine.Pin(6, machine.Pin.OUT)

# ground pin 25 to avoid running program
if stopPin.value() == 0:
    sys.exit()
    
wifi = connection['wifi']
mqtt_broker = connection['BrokerIP']
legControl = jointControl2([13,12,29,28], Kp = [5,5], maxSpeed = [800,800])

for i in range (3):
    try:
        leg = dogLeg(name,wifi,legControl, mqtt_broker)
    except Exception as e:
        if "Wifi connection unsuccessful" in str(e):
            continue
        else:
            led.on()
            raise
    else:
        break

try:
    leg.run()
except Exception as e:
    print(e)

led.on()
    


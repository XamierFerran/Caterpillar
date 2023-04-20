import time
import machine
from secrets import brokerIP as mqtt_broker
import mqtt_CBR
from queue import queue
from Paths import *
from jointControl import *
import Testing as T
from Paths import *

swingPath = (knee[0:50],[x*-1 for x in shoulder[0:50]])
underPath = (knee[51:54],[x*-1 for x in shoulder[51:54]])
backPath = (knee[54:58],[x*-1 for x in shoulder[54:58]])

class dogLeg():
    def __init__(self, name, wifi, legControl):
        self.name = name
        self.led = machine.Pin(6, machine.Pin.OUT)

        mqtt_CBR.connect_wifi(wifi)
        self.blink()
        time.sleep(0.2)
        self.blink()
        time.sleep(0.2)
        self.blink(1)

        self.messages = queue()

        self.client = mqtt_CBR.mqtt_client(name, mqtt_broker, self._whenCalled)
        self.client.subscribe(name)
        self.legControl = legControl

        self.client.publish("updates",f"{name}: Connected" )
        
    
    def blink(self, delay = 0.1):
        self.led.on()
        time.sleep(delay)
        self.led.off()
    
    def _whenCalled(self, topic, msg):
        print("New Message:")
        print((topic.decode(), msg.decode()))
        if self.messages.full():
            self.client.publish("updates",f"{self.name}: Queue Full")
            return
        self.messages.put(msg.decode())
        self.blink()
    
    def run(self):
        while True:
            try:
                self.client.check()
                if not self.messages.empty():
                    message = self.messages.get()
                    if message == "swing":
                        self._runPath(swingPath)
                    elif message == "moveUnder":
                        self._runPath(underPath)
                    elif message == "moveBack":
                        self._runPath(backPath)
                else:
                    self.legControl.continuePrev()

            # except OSError as e:
            #     print(e)
            #     self.client.connect()
            except KeyboardInterrupt as e:
                self.client.disconnect()
                print('done')
                break
    
    def stop(self):
        self.legControl.stop()
    
    #### not tested #####
    def _runPath(self, path, moveTime = 50):
        for i in range(len(path[0])):
            self.legControl.setAngles([path[0][i],path[1][i]],moveTime)

    

    



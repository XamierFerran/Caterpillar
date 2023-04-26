import time
import machine
import mqtt_CBR
from queue import queue
from Paths import *
from jointControl2 import *
import Testing as T
from Paths import *

swingPath = (knee[0:50],shoulder[0:50])
underPath = (knee[51:54],shoulder[51:54])
backPath = (knee[54:58],shoulder[54:58])

class dogLeg():
    def __init__(self, name, wifi, legControl, mqtt_broker):
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
        print("1")
        self.legControl = legControl
        print("2")

        self.client.publish("updates",f"{name}: Connected")
        print("4")
        
    
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
        tick = time.ticks_ms()
        while True:
            print("2")
            try:
                print("3")
                self.client.check()
                print("4")
                if not self.messages.empty():
                    print("5")
                    message = self.messages.get()
                    # moves the leg to the first position in a path
                    if "moveToStart" in message:
                        pathname = message.split("moveToStart ")[1]
                        if pathname == "swing":
                            self.legControl.setAngles([swingPath[0][0],swingPath[1][0]],1000)
                        elif pathname == "moveUnder":
                            self.legControl.setAngles([underPath[0][0],underPath[1][0]],1000)
                        elif pathname == "moveBack":
                            self.legControl.setAngles([backPath[0][0],backPath[1][0]],1000)
                    elif message == "swing":
                        self._runPath(swingPath)
                    elif message == "moveUnder":
                        self._runPath(underPath)
                    elif message == "moveBack":
                        self._runPath(backPath)
                    elif message == "turnOff":
                        self.stop()
                        break
                else:
                    self.legControl.continuePrev(100)
                    time.sleep(0.01)
                
                # keep connection to broker alive
                if time.ticks_ms() > tick + 5000:
                    self.client.ping()
                    tick = time.ticks_ms()
                    print("ping")

            except OSError as e:
                print(e)
                # self.client.connect()
                self.stop()
                raise
            except KeyboardInterrupt as e:
                self.stop()
                self.client.disconnect()
                print('done')
                break
    
    def stop(self):
        self.legControl.stop()
    
    def _runPath(self, path, moveTime = 50):
        for i in range(len(path[0])):
            self.legControl.setAngles([path[0][i],path[1][i]],moveTime)

    

    



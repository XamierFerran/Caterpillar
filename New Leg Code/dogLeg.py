import time
import machine
import mqtt_CBR
from queue import queue
from Paths import *
from jointControl2 import *
import Testing as T
from Paths import *

swingPath = (knee[0:50],shoulder[0:50])
underPath = (knee[50:54],shoulder[50:54])
backPath = (knee[54:58],shoulder[54:58])

class dogLeg():
    def __init__(self, name, wifi, legControl, mqtt_broker):
        self.name = name
        self.led = machine.Pin(6, machine.Pin.OUT)
        
        mqtt_CBR.connect_wifi(wifi)

        #visual confirmation for wifi connection
        self.blink()
        time.sleep(0.2)
        self.blink()
        time.sleep(0.2)
        self.blink(1)

        self.messages = queue()

        self.client = mqtt_CBR.mqtt_client(name, mqtt_broker, self._whenCalled)
        self.client.subscribe(name)
        
        self.legControl = legControl

        # publish that leg has been connected
        self.client.publish("updates",f"{name}: Connected")
        
    # blinks onboard light
    def blink(self, delay = 0.1):
        self.led.on()
        time.sleep(delay)
        self.led.off()
    
    # mqtt callback function
    def _whenCalled(self, topic, msg):
        print("New Message:")
        print((topic.decode(), msg.decode()))
        if self.messages.full():
            self.client.publish("updates",f"{self.name}: Queue Full")
            return
        self.messages.put(msg.decode())
        self.blink()
    
    # main control loop for leg
    def run(self):
        tick = time.ticks_ms()
        while True:
            try:
                # check for messages and act on them
                print("check")
                self.client.check()
                print("checked")
                if not self.messages.empty():
                    message = self.messages.get()

                    if message == "turnOff":
                        self.stop()
                        break
                    
                    # follow specific paths
                    elif message == "swing":
                        self._runPath(swingPath)
                    elif message == "moveUnder":
                        self._runPath(underPath)
                    elif message == "moveBack":
                        self._runPath(backPath)

                    # Moves the leg to the first position in a path
                    elif "moveToStart" in message:
                        pathname = message.split("moveToStart ")[1]
                        if pathname == "swing":
                            self.legControl.setAngles([swingPath[0][0],swingPath[1][0]],1000)
                        elif pathname == "moveUnder":
                            self.legControl.setAngles([underPath[0][0],underPath[1][0]],1000)
                        elif pathname == "moveBack":
                            self.legControl.setAngles([backPath[0][0],backPath[1][0]],1000)

                    # Moves elbow and shoulder to desired angle. Expects message format: moveToAng 45 45"
                    elif "moveToAng" in message:
                        angs = message.split()[1:3]
                        angs = [float(i) for i in angs]
                        self.legControl.setAngles(angs,1000)

                # If no update, hold last position
                else:
                    self.legControl.continuePrev(500)
                    time.sleep(0.01)
                
                # keep connection to broker alive
                if time.ticks_ms() > tick + 5000:
                    self.client.ping()
                    tick = time.ticks_ms()
                    print("ping")
            
            # Make sure motors are stopped before exception reraised
            except OSError as e:
                print(e)
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

    

    



import time
import machine
from secrets import brokerIP as mqtt_broker
import mqtt_CBR
from queue import queue

class dogLeg():
    def __init__(self, name, wifi):
        self.name = name
        self.led = machine.Pin(6, machine.Pin.OUT)

        mqtt_CBR.connect_wifi(wifi)
        self.blink()
        time.sleep(0.2)
        self.blink()
        time.sleep(0.2)
        self.blink(1)

        self.client = mqtt_CBR.mqtt_client(name, mqtt_broker, self._whenCalled)
        self.client.subscribe(name)
        self.client.publish("updates",f"{name}: Connected" )

        self.messages = queue()
    
    def blink(self, delay = 0.1):
        self.led.on()
        time.sleep(delay)
        self.led.off()
    
    def _whenCalled(self, topic, msg):
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
                        print("1")
                        pass
                    elif message == "moveUnder":
                        print("2")
                        pass
                    elif message == "moveBack":
                        print("3")
                        pass

            except OSError as e:
                print(e)
                self.client.connect()
            except KeyboardInterrupt as e:
                self.client.disconnect()
                print('done')
                break
    

    



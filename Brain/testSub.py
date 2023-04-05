import paho.mqtt.client as mqtt
import time
from secrets import BrokerIP

client = mqtt.Client("testSubscriber")

client.connect(BrokerIP)

def what(who,user,msg):
    print("Topic: " + msg.topic + "    Message: " + msg.payload.decode())

client.on_message = what
client.subscribe("#")
client.loop_forever()
import paho.mqtt.client as mqtt
import time
from secrets import BrokerIP
import sys

args = sys.argv
if len(args) > 1:
    topic = sys.argv[1]
else:
    topic = "#"

client = mqtt.Client("testSubscriber")

client.connect(BrokerIP)

def what(who,user,msg):
    print("Topic: " + msg.topic + "    Message: " + msg.payload.decode())

client.on_message = what
client.subscribe(topic)
client.loop_forever()
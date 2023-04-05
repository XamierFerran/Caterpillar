# File to quickly publish messages over mqtt for testing from command line
# syntax from command line is: python3 testPub.py [topic] [message]
import paho.mqtt.client as mqtt
from secrets import BrokerIP
import sys

args = sys.argv
if len(args) != 3:
    print("Must specify a topic and a message")
    exit()

client = mqtt.Client("Tester")
client.connect(BrokerIP)
client.publish(args[1],args[2])
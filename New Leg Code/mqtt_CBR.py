from umqtt.simple import MQTTClient
import network, ubinascii
from socket import socket
import urequests as requests
import time
import machine

def connect_wifi(wifi):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
    print("MAC " + mac)
    
    if wifi['pass']== '':
        station.connect(wifi['ssid'], timeout = 10)
    else:
        station.connect(wifi['ssid'],wifi['pass'])
    
    tick = time.ticks_ms()
    while not station.isconnected():
        time.sleep(1)
        if time.ticks_ms() > tick + 10000:
            raise Exception("Wifi connection unsuccessful")
    print('Connection successful')
    print(station.ifconfig())
    
def chuck_check():
    r=requests.get('https://api.chucknorris.io/jokes/random')
    data = r.json()
    print(data)

class mqtt_client():
    def __init__(self, my_id, serverURL, callback_function):
        self.URL = serverURL
        self.id = my_id
        self.client = None
        self.callback = callback_function
        self.try_to_connect()
        
    def try_to_connect(self):
        try:
            self.client = MQTTClient(self.id, self.URL, keepalive=60)
            self.client.connect()
            self.client.set_callback(self.callback)
            print('Connected to %s MQTT broker' % (self.URL))
            return True
        except OSError as e:
            print('Failed to connect to %s' % (self.URL))
            return False
            
    def connect(self):
        while not self.try_to_connect():
            print('restarting...')
            time.sleep(10)
            machine.reset()
            
    def check(self):
        self.client.check_msg()
            
    def disconnect(self):
        self.client.disconnect()

    def subscribe(self, topic_sub):
        print(topic_sub)
        self.client.subscribe(topic_sub.encode())
    
    def publish(self, topic_pub, msg):
        self.client.publish(topic_pub.encode(),msg.encode())
    
    def ping(self):
        self.client.ping()


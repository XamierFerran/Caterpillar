import network, time
from mqtt import MQTTClient

# Set up Wi-Fi connection
wifi_ssid = "tufts_eecs"
wifi_password = "foundedin1883"
IPAdd = "10.247.57.85"

print("Trying to connect. Note this may take a while...")

wlan = network.WLAN(network.STA_IF)

print(wlan.scan())

wlan.deinit()
wlan.active(True)
wlan.connect(wifi_ssid, wifi_password, timeout=30000) #keepalive=60

print("WiFi Connected ", wlan.ifconfig())
print("Test4")
client = MQTTClient("openmv",IPAdd, port=1883, keepalive=60)
print("Test3")
client.connect()
print("Test2")

while (True):
    client.publish("test", "Hello World!")
    print("Test1")
    time.sleep_ms(1000)

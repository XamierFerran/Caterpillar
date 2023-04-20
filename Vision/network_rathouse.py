import network, time
from mqtt import MQTTClient

# Set up Wi-Fi connection
wifi_ssid = "rat house"
wifi_password = "CommonPolybody256"
IPAdd = "10.0.0.179"

print("Trying to connect. Note this may take a while...")

wlan = network.WLAN(network.STA_IF)

#print(wlan.scan())

print("Test8")

wlan.deinit()
print("Test7")
wlan.active(True)
print("Test6")
wlan.connect(wifi_ssid, wifi_password, timeout=30000)

print("Test5")

print("WiFi Connected ", wlan.ifconfig())
print("Test4")
client = MQTTClient("openmv", IPAdd, port=1883, keepalive=60)
print("Test3")
client.connect()
print("Test2")

while (True):
    client.publish("test", "Hello World!")
    print("Test1")
    time.sleep_ms(1000)

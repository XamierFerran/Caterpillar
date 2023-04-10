import time
from machine import UART
import mqtt_CBR # check if this import works
from secrets import Tufts_Wireless as wifi # remember secrets.py file

# SETUP
mqtt_broker = '192.168.86.23' # change
topic = 'ESP/listen' # change
client_id = 'MyESP'

mqtt_CBR.connect_wifi(wifi)
led = machine.Pin(2, machine.Pin.OUT)

uart = UART(1, baudrate=115200)

# FUNCTIONS
def blink(delay = 0.1):
    led.off()
    time.sleep(delay)
    led.on()
    
def whenCalled(topic, msg):
    print((topic.decode(), msg.decode()))
    blink()
    time.sleep(0.5)
    blink()
        
def main():
    fred = mqtt_CBR.mqtt_client(client_id, mqtt_broker, whenCalled)
    fred.subscribe(topic_sub)

    old = 0
    i = 0
    while True:
        try:
            fred.check()
            if (time.time() - old) > 5:
                msg = 'iteration %d' % i
                fred.publish(topic_pub, msg)
                old = time.time()
                i += 1
                blink()
        except OSError as e:
            print(e)
            fred.connect()
        except KeyboardInterrupt as e:
            fred.disconnect()
            print('done')
            break

# EXECUTION
# while True:
text = uart.readln()
print(text, end='')
time.sleep(0.1)
main()
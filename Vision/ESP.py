import time
from machine import UART
import Serial

s = Serial.serial_comm(115200)

while True:
        if s.any():
            text = s.readln()
            print(text, end='')
        time.sleep(0.1)

# publish to MQTT (use temp values)
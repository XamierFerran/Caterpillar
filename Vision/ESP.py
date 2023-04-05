import time
from machine import UART
import Serial

s = Serial.serial_comm(115200)

# read in serial data
# publish to MQTT (use temp values)
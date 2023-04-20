#Enter code v python3

# This example shows a simple way to control the Motoron Motor Controller.
# It is like serial_simple_example.py but it does not use the Motoron library.

import math
import time
from machine import UART, Pin, PWM
import utime

port = UART(0, 115200, timeout = 100)

class Count(object):
    def __init__(self,A,B):
        self.A = A
        self.B = B
        self.counter = 0
        A.irq(self.cb,self.A.IRQ_FALLING|self.A.IRQ_RISING) #interrupt on line A
        B.irq(self.cb,self.B.IRQ_FALLING|self.B.IRQ_RISING) #interrupt on line B

    def cb(self,msg):
        other,inc = (self.B,1) if msg == self.A else (self.A,-1) #define other line and increment
        self.counter += -inc if msg.value()!=other.value() else  inc #XOR the two lines and increment
        
    def value(self):
        return self.counter
                
    def reset(self):
        self.counter = 0
        
# Sets max acceleration of the motor input
def set_max_acceleration(motor, accel):
    accel_array = [156, motor, 10, accel & 127, (accel >> 7) & 127, 156, motor, 12, accel & 127, (accel >> 7) & 127]
    byte_accel_array = bytearray()
    for i in accel_array:
        byte_accel_array.append(i)
    port.write(bytes(byte_accel_array))

# Sets max deceleration of the motor input
def set_max_deceleration(motor, decel):
    decel_array = [156, motor, 14, decel & 127, (decel >> 7) & 127, 156, motor, 16, decel & 12, (decel >> 7) & 127]
    byte_decel_array = bytearray()
    for i in decel_array:
        byte_decel_array.append(i)
    port.write(bytes(byte_decel_array))
        
# This sets the speed of the motor that you input, between 0 and 800
def set_speed(motor, speed):
    speed_array = [209, motor, speed & 127, (speed >> 7) & 127]
    byte_speed_array = bytearray()
    for i in speed_array:
        byte_speed_array.append(i)
    port.write(bytes(byte_speed_array))

# This resets the motor controller board
reset_array = [150, 116, 139, 4, 123, 67, 169, 0, 4]
byte_reset_array = bytearray()
for i in reset_array:
    byte_reset_array.append(i)
port.write(bytes(byte_reset_array))

# This command disables the function that tells the motor to stop spinning after 1 second
disable_array = [156]
byte_disable_array = bytearray()
for i in disable_array:
    byte_disable_array.append(i)

byte_disable_array.append(0)
byte_disable_array.append(8)
byte_disable_array.append(0)
byte_disable_array.append(4)
port.write(bytes(byte_disable_array))



# Configure motor 1
set_max_acceleration(1, 0)
set_max_deceleration(1, 0)

# Configure motor 2
set_max_acceleration(2, 0)
set_max_deceleration(2, 0)

# Motor 1 encoder A output = pin D4, GPIO16
# Motor 1 encoder B output = pin D5, GPIO17

# Motor 2 encoder A output = pin D2, GPIO25
# Motor 2 encoder B output = pin D3, GPIO15






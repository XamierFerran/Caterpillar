# uses threading instead of motor controller board to do encoder counts
import time
import Testing as T
import os
from encoderThread import *
#[13,12,29,28]
class jointControl2():
    def __init__(self, encoderPins, Kp = [1,1], maxSpeed = [100,100]):

        if len(Kp) != 2:
            raise Exception("Error: please input 2 Kp values")
        
        if len(maxSpeed) != 2:
            raise Exception("Error: please input 2 maxSpeed values")

        self.lastAngles = [0,0]

        self.Kp = Kp
        self.dutyMax = maxSpeed

        #encoder counts per degree
        self.corr = 1632/360

        self.encoders = encoderThread(encoderPins)
        self.encoders.run()
    
    
    def setAngles(self, angles, moveTime = 500, Print = False):
        if len(angles) != 2:
            print("setAngles: angles list size must be 2")
            return
        
        self.lastAngles = angles

        # initialize values
        goalCounts = []
        errors = []
        power = []
        for i in range(2):
            currEncode = self.encoders.readEncoder(i)

            #Initial error
            goalCounts.append(angles[i]*self.corr)
            errors.append(goalCounts[i] - currEncode)

            #Initial power
            power.append(int(self.Kp[i]*(errors[i])))
            power[i] = max(-1*self.dutyMax[i], (min(power[i], self.dutyMax[i])))
            T.set_speed(i+1, power[i])
        

        # proportional control loop
        initialTime = time.ticks_ms()
        while initialTime + moveTime > time.ticks_ms():
            for i in range(2):

                currEncode = self.encoders.readEncoder(i)

                errors[i] = goalCounts[i] - currEncode
                power[i] = int(self.Kp[i]*(errors[i]))
                power[i] = max(-1*self.dutyMax[i], (min(power[i], self.dutyMax[i])))
                T.set_speed(i+1, power[i])

                if Print:
                    print(self.encoders.readEncoder(i))
                    print(goalCounts[i])
                    print()

    
    def continuePrev(self, moveTime = 500):
        self.setAngles(self.lastAngles, moveTime)

    def stop(self):
        T.set_speed(1,0)
        T.set_speed(2,0)
    
    def reset(self):
        for motor in self.motors:
            b = motor.resetEncoder(0)

    def encoderTest(self, moveTime = 1000):
        initialTime = time.ticks_ms()
        while initialTime + moveTime > time.ticks_ms():
            for i in range(2):
                print(self.encoders.readEncoder(i))
                print()
                i += 1
            print()
            time.sleep_ms(500)
            
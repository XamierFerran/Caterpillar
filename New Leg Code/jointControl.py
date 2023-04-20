import time
from motorController import *
import Testing as T
import os

class jointControl():
    def __init__(self, motors, Kp = [1,1], maxSpeed = [100,100]):

        self.motors = motors
        if len(Kp) != len(self.motors):
            raise Exception("Error: Kp list size must match motors")
        
        if len(maxSpeed) != len(self.motors):
            raise Exception("Error: maxSpeed list size must match motors")

        self.lastAngles = [0]*len(self.motors)

        self.Kp = Kp
        self.dutyMax = maxSpeed
        for motor in self.motors:
            b = motor.resetEncoder(0)

        #encoder counts per degree
        self.corr = 1632/360
    
    
    def setAngles(self, angles, moveTime = 500, Print = False):
        if len(angles) != len(self.motors):
            print("setAngles: angles list size must match motors")
            return
        
        self.lastAngles = angles

        # initialize values
        goalCounts = []
        errors = []
        power = []
        i = 0
        for motor in self.motors:

            # keep trying to get first encoder value, if connections aren't
            # perfect occasionally bad data will cause an error to be thrown
            while True:
                try:
                    currEncode = motor.readEncoder()
                    break
                except OSError as e:
                    if e.errno == 5:
                        print("OS errno 5 caught in beginning setAngles")
                        continue
                    else:
                        print("err1")##################
                        raise
                except TypeError as e:
                    if "can't convert 'int' object to str implicitly" in str(e.args):
                        print("Caught TypeError in beginning setAngles")
                    else:
                        print("err2")##################
                        raise

            
            #Initial error
            goalCounts.append(angles[i]*self.corr)
            errors.append(goalCounts[i] - currEncode)

            #Initial power
            power.append(int(self.Kp[i]*(errors[i])))
            power[i] = max(-1*self.dutyMax[i], (min(power[i], self.dutyMax[i])))
            T.set_speed(i+1, power[i])
            i += 1
        

        # proportional control loop
        initialTime = time.ticks_ms()
        while initialTime + moveTime > time.ticks_ms():
            i = 0
            for motor in self.motors:

                # if getting encoder value raises expected exception, Ignore
                try:
                    # print("read2")##################
                    currEncode = motor.readEncoder()
                    # print("stopread2")##################
                except OSError as e:
                    if e.errno == 5:
                        print("OS errno 5 caught in loop setAngles")
                    else:
                        print("err3")##################
                        raise
                except TypeError as e:
                    if "can't convert 'int' object to str implicitly" in str(e.args):
                        print("Caught TypeError in loop setAngles")
                    else:
                        print("err4")##################
                        raise


                errors[i] = goalCounts[i] - currEncode
                power[i] = int(self.Kp[i]*(errors[i]))
                power[i] = max(-1*self.dutyMax[i], (min(power[i], self.dutyMax[i])))
                T.set_speed(i+1, power[i])

                if Print:
                    print(motor.readEncoder())
                    print(goalCounts[i])
                    print()
                i += 1

    
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
            i = 0
            for motor in self.motors:
                print(motor.readEncoder())
                print()
                i += 1
            print()
            time.sleep_ms(500)


        
            

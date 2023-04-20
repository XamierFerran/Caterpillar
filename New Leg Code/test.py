from jointControl import *
import Testing as T
from Paths import *

leg  = jointControl([DCMotor(1),DCMotor(0)], Kp = [1,1], maxSpeed = [800,800])
shoulder = [-1 * x for x in shoulder]

leg.setAngles([-75,-56],50)

for i in range(10000):
    leg.continuePrev(5)

leg.stop()

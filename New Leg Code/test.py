from jointControl2 import *
import Testing as T
from Paths import *

leg  = jointControl2([13,12,29,28], Kp = [5,5], maxSpeed = [400,400])

#leg.setAngles([-75,-56],50)

#for i in range(10000):
#    leg.continuePrev(5)

leg.stop()


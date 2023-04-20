from dogLeg import *
from secrets import TuftsWireless as wifi
from motorController import *
from jointControl import *

legControl = jointControl([DCMotor(1),DCMotor(0)], Kp = [5,5], maxSpeed = [800,800])

leg = dogLeg("frontRight",wifi,legControl)

leg.run()

#### catching os error 5 in setangle doesnt work

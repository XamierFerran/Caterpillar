import _thread
import machine
import time

class encoderThread():
    def __init__(self, e1a, e1b, e2a, e2b):
        self.e1a = machine.Pin(e1a, machine.Pin.IN, machine.Pin.Pull_UP)
        self.e1b = machine.Pin(e1b, machine.Pin.IN, machine.Pin.Pull_UP)
        self.e2a = machine.Pin(e2a, machine.Pin.IN, machine.Pin.Pull_UP)
        self.e2b = machine.Pin(e2b, machine.Pin.IN, machine.Pin.Pull_UP)

        self.encoder1Count = 0
        self.encoder2Count = 0

        # not used yet, might try using if I get 
        self.encoder_lock = _thread.allocate_lock()

    def _encoderTask(self):
        a, b = self.e1a.value(), self.e1b.value()
        olda, oldb = a, b
        c, d = self.e2a.value(), self.e2b.value()
        oldc, oldd = c, d

        while True:
            a, b = self.e1a.value(), self.e1b.value()
            c, d = self.e2a.value(), self.e2b.value()

            if a != olda:
                self.encoder1Count += -1 if a == b else  1
                olda = a 
            if b != oldb:
                self.encoder1Count +=  1 if a == b else -1
                oldb = b
            if c != oldc:
                self.encoder2Count += -1 if c == d else  1
                oldc = c
            if d != oldd:
                self.encoder2Count +=  1 if c == d else -1
                oldd = d
    
    def run(self):
        _thread.start_new_thread(self._encoderTask,())
    
    def readEncoder1(self):
        return self.encoder1Count
    
    def readEncoder2(self):
        return self.encoder1Count
            
import _thread
import machine
import time

class encoderThread():
    def __init__(self, encoderPins):
        self.e1a = machine.Pin(encoderPins[0], machine.Pin.IN, machine.Pin.PULL_UP)
        self.e1b = machine.Pin(encoderPins[1], machine.Pin.IN, machine.Pin.PULL_UP)
        self.e2a = machine.Pin(encoderPins[2], machine.Pin.IN, machine.Pin.PULL_UP)
        self.e2b = machine.Pin(encoderPins[3], machine.Pin.IN, machine.Pin.PULL_UP)

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
                try:
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

                
                except Exception as e:
                    print("In encode thread:")
                    print(e)
                    
                    if "could not connect" in str(e):
                        continue
                    else:
                        raise
    
    def run(self):
        _thread.start_new_thread(self._encoderTask,())
    
    def readEncoder(self, num):
        if num == 0:
            return self.encoder1Count
        if num == 1:
            return self.encoder2Count
 
 
# Implementing a circular buffer queue data structure I can use for storing commands 
# from mqtt on the rp2040s because micropython doesn't have queues for some reason
class queue():
    def __init__(self, maxSize = 10):
        self.array = ['']*maxSize
        self.maxSize = maxSize
        self.front = 0
        self.back = 0
        self.size = 0

    def put(self, data):
        if self.size == self.maxSize:
            raise Exception("Put failed: queue full")
        
        self.array[self.back] = data
        self.back = (self.back+1)%self.maxSize
        self.size = self.size +1

    def get(self):
        if self.empty():
            raise Exception("Get failed: queue empty")
        
        data = self.array[self.front]
        self.front = (self.front+1)%self.maxSize
        self.size = self.size -1

        return data
        
    def empty(self):
        if self.size == 0:
            return True
        else:
            return False
    
    def full(self):
        if self.size == self.maxSize:
            return True
        else:
            return False

import threading

#Bounded Buffer Queue
class BBQ:
    def __init__(self):
        self.queue = []
        self.lock = threading.Lock()
        #semaphore for items in the buffer
        self.data = threading.Semaphore(0)
        #semaphore for counting the number of slots in the buffer
        self.empty = threading.Semaphore(10)

    def dequeue(self):
        #consumer must wait before reading from the buffer
        self.data.acquire()
        self.lock.acquire()
        val = self.queue.pop(0)
        self.lock.release()
        #consumer will signal semaphore after reading buffer
        self.empty.release()
        return val

    def enqueue(self, val):
        #producer must wait for a slot to write to the buffer
        self.empty.acquire()
        self.lock.acquire()
        self.queue.append(val)
        self.lock.release()
        #data will signal after writing to the buffer
        self.data.release()
    
    def is_empty(self):
        if not self.queue:
            return True
        return False
        
    
    


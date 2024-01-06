# Fill the class given below for the first part of the assignment
# You can add new functions if necessary
# but don't change the signatures of the ones included
import threading
import random

class ConSet:
    def __init__(self):
        self.data = {}  # Dictionary to store elements
        self.lock = threading.Lock()
        self.empty = threading.Condition(self.lock)
        self.pop_waiting = 0

    def insert(self, newItem):
        with self.lock:
            self.data[newItem] = True
            self.empty.notify()
        
    def pop(self):
        while True:
            with self.lock:
                available_keys = [key for key, val in self.data.items() if val]

                if available_keys != []:
                    elt = random.choice(available_keys)
                    self.data[elt] = False
                    return elt
                else:
                    self.pop_waiting += 1
                    if self.pop_waiting == 1:
                        self.empty.wait()
                    self.pop_waiting -= 1

    def printSet(self):
        print(self.data)




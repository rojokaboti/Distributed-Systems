import threading
import random

class ConSet:
    def __init__(self):
        self.data = {}  # Dictionary to store elements
        self.lock = threading.Lock()
        self.empty = threading.Condition(self.lock)
        self.pop_waiting = 0

    def insert(self, elt):
        with self.lock:
            self.data[elt] = True
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


##Testing 

"""
def insert(node_id, mailbox):
    mailbox.insert(node_id)
    print(mailbox.data)

def pop(mailbox):
    mailbox.pop()
    print(mailbox.data)

if __name__ == '__main__':
    n = 10  # Number of nodes inserting
    m = 10  # Number of nodes popping
    mailbox = ConSet()
    threads = []

    # Create threads for inserting elements
    for i in range(n):
        thread = threading.Thread(target=insert, args=(i, mailbox))
        threads.append(thread)
        thread.start()

    # Create threads for popping elements
    for i in range(m):
        thread = threading.Thread(target=pop, args=(mailbox,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

   """ 
from ConSet import *
import random


def node_work(node_id, n, mailboxes, barrier):
    assert isinstance(node_id, int) and node_id >= 0 #Making sure the node id in a non-negative integer
    
    def gen_val():                            #generating a random int between 0 and n^2
        return random.randint(0, n * n)
    
    leader_cand = []
    round = 0

    while len(leader_cand) != 1:

        barrier.wait()   #Making sure all thread printed results from last round
        round += 1       
        val = gen_val()
        message = (val, node_id)

        print(f"Node {node_id} proposes value {val} for round {round}.")   #Printing the proposed value of this node for this round

        for mailbox in mailboxes:        #Adding this node's proposed value to all mailboxes
            mailbox.insert(message)  


        received_messages = []
        for i in range(n):          #Reading all recieved messages from other nodes and appending them to a list
            received_message = mailboxes[node_id].pop()
            received_messages.append(received_message)

        max_val = max(received_messages, key=lambda x: x[0])   #fiding max value proposed between all nodes
        leader_cand = [message[1] for message in received_messages if message[0] == max_val[0]]  #fiding all nodes that proposed the maximal value
        
        if len(leader_cand) > 1:        #If more than one node proposes the same maximal value, we move to next round
            print(f"Node {node_id} could not decide on the leader and moves to round {round+1}.")
        

    print(f"Node {node_id} decided {leader_cand[0]} as the leader.")



# This is a testing section, unquote fo testing 
"""
if __name__ == '__main__':
    n = 3  # Number of nodes
    barrier = threading.Barrier(n)
    mailboxes = [ConSet() for _ in range(n)]
    threads = []

    for i in range(n):
        thread = threading.Thread(target=node_work, args=(i, n, mailboxes, barrier))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

"""
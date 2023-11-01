from ConSet import *
import random

def node_work(node_id, n, mailboxes):
    def gen_val():
        return random.randint(0, n * n)

    while True:
        val = gen_val()
        message = (val, node_id)

        for mailbox in mailboxes:
            mailbox.insert(message)

        received_messages = []
        for i in range(n):
            received_message = mailboxes[node_id].pop()
            received_messages.append(received_message)

        max_val = max(received_messages, key=lambda x: x[0])
        leader_cand = [message[1] for message in received_messages if message[0] == max_val[0]]

        if len(leader_cand) == 1:
            print(f"Node {node_id} is the leader.")
            break


##Testing 

"""
if __name__ == '__main__':
    n = 5  # Number of nodes
    mailboxes = [ConSet() for _ in range(n)]
    threads = []

    for i in range(n):
        thread = threading.Thread(target=node_work, args=(i, n, mailboxes))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print([m.data for m in mailboxes])
"""
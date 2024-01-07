import sys
import multiprocessing as mp
import zmq


def get_param():
    # This function reads the argumets given in command line 
    # and prints them at the end with some formatting
    if len(sys.argv) != 4:
        print("Usage: python3 paxos.py [number of nodes] [probability of a crash] [number of rounds]")
        sys.exit(1)
    try:
        num_nodes = int(sys.argv[1])
        crash_prob = float(sys.argv[2])
        num_rounds = int(sys.argv[3])
        round = 0
        if crash_prob>1 or crash_prob<0:
            print('The given crash probability is not valid!')
        else:
            print(f"NUM NODES: {num_nodes}, CRASH PROB: {crash_prob}, NUM ROUNDS: {num_rounds}")      
    except:
        print('One or more of the parameters is incorrect!')

    return num_nodes, crash_prob, num_rounds

class PaxosNode:        
    def __init__(self,ID: int, prob:float , num_nodes:int, val:int , numRounds:int):
        self.ID = ID
        self.prob = prob
        self.num_nodes = num_nodes
        self.val = val
        self.numRounds = numRounds
        self.maxVotedRound = -1
        self.maxVotedVal = None
        self.proposeVal = None
        self.decision = None
        self.leader = False
        self.barrier = mp.Barrier(num_nodes)
        

    def network(self):
        ID = self.ID
        N = self.N
        context = zmq.Context()

        #Adding single pull socket
        pull_socket = context.socket(zmq.PULL)
        pull_socket.bind("tcp://127.0.0.1:5550"+str(self.ID))

        #Adding N push sockets for every node in the network.
        push_sockets = {}
        for i in range(N):
            push_socket = context.socket(zmq.PUSH)
            push_socket.bind("tcp://127.0.0.1:5550"+str(i))
            push_sockets[i] = push_socket

        return pull_socket, push_sockets

        
    def recieve_msg(self, pull_socket):
        while True:
            message = pull_socket.recv_string()
            print(f"Received: {message}")

            
    def broadcast_msg(self, push_sockets, msg, proposer, N, prob):
        for push_socket in push_sockets.values():
            target = push_socket
            self.sendFailure (msg, proposer, target, prob)


    def send(self, msg, target):
        print(msg)

    
    def sendFailure (self, msg, proposer, target, prob):
        self.send(msg)

    def broadcast_failure(self, msg, proposer, num_nodes, prob):
        self.send(msg)



"""It first broadcasts a START message using broadcastFailure method de-
scribed above. Since the broadcast is done by broadcastFailure method,
each acceptor might nondeterministically receive a START or "CRASH r%N"
3
message representing temporary crashes of the proposer. Since nodes are
synchronized, you do not have to attach round number to the START mes-
sage.
• The proposer blocks for receiving N messages (including one from itself
as well) and keeps the JOIN count for these messages. There are three
types of possible incoming messages: They can start with JOIN, CRASH or
START. Receiving its own START message is interpreted as a successful join
to this round. If the proposer does not receive a START message, it receives
a CRASH for its place which will interpreted as failure of this node as an
acceptor as well. Note that the proposer always receives N messages in
total.
• If the total number of JOIN and START messages are bigger than N/2,
then the proposer picks the JOIN message with the maxV otedRound field
and sets the proposeV al as maxV otedV al of this message. If it has re-
ceived a START message from itself, its own local maxV otedRound and
maxV otedV al variables are taken into consideration for the computation
of proposeV al. If the resulting maxV otedRound is −1 meaning that none
of the nodes in the join quorum has voted before, then the proposer n sets
proposeV al to val (input of the PaxosNode method). Then, it broadcasts
"PROPOSE proposeV al" message using broadcastFailure method.
• If the total number of JOIN and START messages are less than or equal to
N/2, then the proposer broadcasts a ROUNDCHANGE message to all nodes
and moves directly to the next round. ROUNDCHANGE message is sent for
establishing the synchronization among nodes. Therefore, it must not be
sent using the broadcastFailure and directly sent to all nodes (except itself)
without any failure possibility.
• If n has previously decided to send a PROPOSE message, it blocks for receiv-
ing N messages. The possible messages it can get start with VOTE, CRASH
or PROPOSE. If it receives its own PROPOSE message, it can be thought as a
positive VOTE response to itself and then it updates the maxV otedRound
to r and maxV otedV al to its own proposeV al. If total number of VOTE
and PROPOSE messages are bigger than N/2, this round reaches to a de-
cision and decision becomes proposeV al. After receiving N messages, n
moves to the next round."""
    def leader_process(self):
        pull_socket, push_sockets = self.network()
        msg = f"ROUND {round} STARTED WITH INITIAL VALUE: {self.val}"
        self.broadcast_failure(msg, 1, self.num_nodes, self.prob)  #fix this
        joins = 0
        self_join = False
        for i in range(num_nodes):
            resp = self.recieve_msg()
            if "JOIN" in resp:
                joins += 1
            elif "START" in resp:
                joins += 1
                self_join = True
            else:
                pass
        if (joins > (self.num_nodes/2)) and (self_join == True):
            pass
        else:


    def acceptor_process(self):
        while True:
            msg = self.recieve_msg()
            break

        if "START" in msg:
            print(f"ACCEPTOR {self.ID} RECEIVED IN JOIN PHASE: START")
            resp = f"JOIN {self.maxVotedRound} {self.maxVotedVal}"
            proposer_id = round%self.num_nodes
            self.sendFailure(resp, proposer_id, self.crash_prob)

        elif "CRASH" in msg:
            proposer_id = round%self.num_nodes
            print(f"ACCEPTOR {self.ID} RECEIVED IN JOIN PHASE: CRASH {proposer_id}")
            resp = f"CRASH {proposer_id}"
            self.send(resp, proposer_id)

        while True:
            msg = self.recieve_msg()
            break

        if "PROPOSE" in msg:
            print(f"ACCEPTOR {self.ID} RECEIVED IN VOTE PHASE: {msg}")
            resp = "VOTE"
            self.sendFailure(resp, proposer_id, self.crash_prob)
            self.maxVotedRound = round
            self.maxVotedVal = msg[1]
            print(f"ACCEPTOR {self.ID} RECEIVED IN VOTE PHASE: ROUNDCHANGE")

        elif "CRASH" in msg:
            print(f"ACCEPTOR {self.ID} RECEIVED IN VOTE PHASE: {msg}")
            resp = "CRASH {proposer_id}"
            self.send(resp, proposer_id)
            print(f"ACCEPTOR {self.ID} RECEIVED IN VOTE PHASE: ROUNDCHANGE")

        else:
            print(f"ACCEPTOR {self.ID} RECEIVED IN VOTE PHASE: ROUNDCHANGE")





    def START(self, round):
        if round % self.num_nodes ==  self.ID:
            self.leader_process()
        else:
            self.acceptor_process()



if __name__ == "__main__":
    #getting parameters from the command line.
    num_nodes, crash_prob, num_rounds = get_param()

    
    
    paxos_nodes = [mp.Process(target=PaxosNode, args=(i)) for i in range(num_nodes)]


    print(paxos_nodes)
        
    


    
        


    

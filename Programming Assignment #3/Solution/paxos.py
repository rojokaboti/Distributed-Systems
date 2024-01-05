import sys
import multiprocessing as mp
import zmq

class PaxosNode(ID, crash_prob, num_nodes, val, num_rounds):        
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


    def send(self, msg):
        print(msg)

    
    def sendFailure (self, msg, proposer, target, prob):
        self.send(msg)

    def broadcast_failure(self, msg, proposer, num_nodes, prob):
        self.send(msg)

    paxos_node = mp.Process(target=self.network, args=())


    def leader_process(self):
        msg = f"ROUND {round} STARTED WITH INITIAL VALUE: {self.val}"
        self.broadcast_failure(msg, 1, self.num_nodes, self.prob)

       
    def START(self, round):
        if round % self.num_nodes ==  self.ID:
            self.leader_process()
        else:
            self.acceptor_process()



if __name__ == "__main__":

# This part reads the argumets given in command line 
# and prints them at the end with some formatting
    if len(sys.argv) != 4:
        print("Usage: python paxos.py [number of nodes] [probability of a crash] [number of rounds]")
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

    barrier = mp.Barrier(num_nodes)
    
    paxos_nodes = [mp.Process(target=PaxosNode, args=(, i)) for i in range(num_processes)]


    print(paxos_nodes)
        
    


    
        


    

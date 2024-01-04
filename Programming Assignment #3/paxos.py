import sys
import multiprocessing as mp
import zmq
from abc import ABC, abstractmethod

round = 0

class PaxosNode(ID, prob, N, val, numRounds):        
    def __init__(self,ID: int, prob:float , N:int, val:int , numRounds:int):
        self.ID = ID
        self.prob = prob
        self.N = N
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


        


    

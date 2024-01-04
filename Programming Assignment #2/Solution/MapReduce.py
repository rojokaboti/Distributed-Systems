# This is MapReduce file

import multiprocessing as mp
import zmq
import json
from abc import ABC, abstractmethod
import pickle


class MapReduce(ABC):
    def __init__(self, num_workers: int):
        self.num_workers = num_workers

    @abstractmethod
    def Map(self, map_input):
        pass

    @abstractmethod
    def Reduce(self, reduce_input):
        pass
 
    def __Producer(self, producer_input):
        context = zmq.Context()
        producer_socket = context.socket(zmq.PUSH)
        producer_socket.bind("tcp://127.0.0.1:5557")

        part_size = len(producer_input) // self.num_workers
        remain = len(producer_input) % self.num_workers

        idx = 0

        for i in range(self.num_workers):
            if remain > 0:
                part = producer_input[idx : idx + part_size + 1]
                remain -= 1
                idx += part_size + 1
            else:
                part = producer_input[idx : idx + part_size]
                idx += part_size

            serialized_part = json.dumps(part)
            producer_socket.send_json(serialized_part) 
        print(f"Producer done!") 

    def __Consumer(self, consumer_id):
        context = zmq.Context()
        consumer_socket = context.socket(zmq.PULL)
        consumer_socket.connect("tcp://127.0.0.1:5557")

        while True:
            message = consumer_socket.recv_json()
            part = json.loads(message) 
            partial_result = self.Map(part)

            serialized_presult = json.dumps(partial_result)

            partial_result_socket = context.socket(zmq.PUSH)
            partial_result_socket.connect("tcp://127.0.0.1:5558")
            partial_result_socket.send_json(serialized_presult)
            print(f"Concumer done!")
                  
    def __ResultCollector(self):
        context = zmq.Context()
        result_socket = context.socket(zmq.PULL)
        result_socket.bind("tcp://127.0.0.1:5558")
        
        partial_results = []
        while True:
            serialized_presult = result_socket.recv_json()
            partial_result = json.loads(serialized_presult)
            
            partial_results.append(partial_result)
            if len(partial_results) == self.num_workers:
                break

        final_result = self.Reduce(partial_results)
        print(f"Final result: {final_result}")
        
        # Write final_result to results.txt
        with open("results.txt", "w") as file:
            file.write(json.dumps(final_result))

        print('result collector done!')
       
    def start(self, filename):
        with open(filename, 'r') as file:
            data = [line.strip().split('\t') for line in file]


        # consumers prossesses
        consumer_processes = []
        for i in range(self.num_workers-1):
            consumer_id = f"Consumer-{i}"
            consumer_process = mp.Process(target=self.__Consumer, args=(consumer_id,))
            consumer_processes.append(consumer_process)
            consumer_process.start()

        #producer process
        producer_process = mp.Process(target=self.__Producer, args=(data,))
        producer_process.start()
            
        
        # result collector process
        result_collector_process = mp.Process(target=self.__ResultCollector)
        result_collector_process.start()        
        

        # Waiting for all processes to finish
        producer_process.join()
        
        for consumer_process in consumer_processes:
            consumer_process.join()
            
        result_collector_process.join() 

        #Terminating all processes
        producer_process.terminate()
        
        for consumer_process in consumer_processes:
            consumer_process.terminate()
            
        result_collector_process.terminate()
        file.close()


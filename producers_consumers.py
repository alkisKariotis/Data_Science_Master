#Final Exam | Question1 | Alkiviadis Kariotis 241735

#Importing Libraries

import threading
import time
from random import randint

#Initializion of semaphores
empty = threading.Semaphore(10)  #Assuming that the buffer size is 10
full = threading.Semaphore(0)
mutex = threading.Lock()

#Creating the shared buffer
buf = []

#Function for the producer thread
def producer(producer_id, iterations, n):
    for i in range(iterations):
        time.sleep(randint(1, 3) / 10)  #Just a random sleep time to simulate the item production process
        item = f"item_{producer_id}_{i}"
        empty.acquire()  #Wait to check if buffer is full
        mutex.acquire()
        buf.append(item)
        print(f"Producer {producer_id} produced {item} to buf")
        mutex.release()
        full.release()  #Send a signal that an item was produced

#Function for the consumer thread
def consumer(consumer_id, iterations):
    for _ in range(iterations):
        full.acquire()  #Wait to check if buffer is empty
        mutex.acquire()
        item = buf.pop(0)
        print(f"Consumer {consumer_id} consumed {item} from buf")
        mutex.release()
        empty.release()  #Send a signal that an item was consumed

def main(n):
    iterations_producer = 2 * n
    iterations_consumer = n
    producers = [threading.Thread(target=producer, args=(i, iterations_producer, n)) for i in range(n)]
    consumers = [threading.Thread(target=consumer, args=(i, iterations_consumer)) for i in range(2 * n)]

    #Start all the producers and the consumers
    for p in producers:
        p.start()
    for c in consumers:
        c.start()

    #Wait for all the producers and the consumers to finish
    for p in producers:
        p.join()
    for c in consumers:
        c.join()

if __name__ == "__main__":
    N = 5  #Just a random number of products to check the script
    main(N)

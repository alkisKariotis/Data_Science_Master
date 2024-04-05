#Final Exam | Question2 | Alkiviadis Kariotis 241735

#Importing Libraries

import threading
import time

def is_perfect(n, perfect_numbers):
    if n < 2:
        return
    divisors_sum = sum([i for i in range(1, n // 2 + 1) if n % i == 0])
    if divisors_sum == n:
        perfect_numbers.append(n)

def find_perfect_numbers(max_num, num_threads):
    start_time = time.time()
    threads = []
    perfect_numbers = []
    for n in range(1, max_num):
        thread = threading.Thread(target=is_perfect, args=(n, perfect_numbers))
        threads.append(thread)
        thread.start()
        #Safety check that we dont exceed the number of specified threads
        if len(threads) >= num_threads:
            for t in threads:
                t.join()
            threads = []

    #Waiting if any remaining threads need to be completed
    for t in threads:
        t.join()

    perfect_count = len(perfect_numbers)
    end_time = time.time()
    print(f"Found {perfect_count} perfect numbers < {max_num} using {num_threads} threads in {end_time - start_time:.2f} seconds.")

#Size of the problem to test
max_nums = [1000, 10000, 100000, 1000000]
#Number of threads to test
threads = [4, 8, 16]

for max_num in max_nums:
    for num_threads in threads:
        find_perfect_numbers(max_num, num_threads)

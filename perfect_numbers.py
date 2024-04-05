#Final Exam | Question2 | Alkiviadis Kariotis 241735

#Importing Libraries

import concurrent.futures
import time

def is_perfect(n):
    if n < 2:
        return False
    divisors_sum = sum([i for i in range(1, n // 2 + 1) if n % i == 0])
    return divisors_sum == n

def find_perfect_numbers(max_num, num_threads):
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        perfect_numbers = list(executor.map(is_perfect, range(1, max_num)))
    perfect_count = sum(perfect_numbers)
    end_time = time.time()
    print(f"Found {perfect_count} perfect numbers < {max_num} using {num_threads} threads in {end_time - start_time:.2f} seconds.")

#Size of the problem to test
max_nums = [1000, 10000, 100000, 1000000]
#Number of threads to test
threads = [4, 8, 16]

for max_num in max_nums:
    for num_threads in threads:
        find_perfect_numbers(max_num, num_threads)
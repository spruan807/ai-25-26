import time, math, cProfile, sys
from pstats import SortKey

new_limit = 1000
sys.setrecursionlimit(new_limit)
print(f"current recursion limit: {new_limit}")

cache = {1:0, 2:1}
times = {}

def collatz(n):
    steps = 0
    nextN = 0
    
    if n%2==0: 
        nextN = n//2
    else:
        nextN = 3*n + 1
    
    if nextN not in cache:
        cache[nextN] = collatz(nextN)
        
    cache[n] = steps = 1 + cache[nextN]
    
    return cache[n]
    
def timer(n):
    start = time.process_time()
    collatz(n)
    elapsed = time.process_time() - start

    return elapsed

def runTrials(n):
    for x in range(1, n):
        times[x] = timer(x)

def dataDisp(n): 
    runTrials(n)

    for k,v in times.items():
        print(f"{k}: {v} sec")

dataDisp(1000)
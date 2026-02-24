import heapq, timeit, random

rands = [ random.randrange(51) for x in range(50000) ]

pq = []
otherlist = []
heapq.heappush(pq,20)
heapq.heappush(pq,5)
heapq.heappush(pq,6)

for n in range(3):
    print(heapq.heappop(pq))

def test_pq():
    heapq.heappush(pq, rands.pop())
    heapq.heappush(pq, rands.pop())
    heapq.heappop(pq)

def test_list():
    otherlist.append(rands.pop())
    otherlist.append(rands.pop())
    sorted(otherlist, reverse=True)
    otherlist.pop()

print(timeit.timeit(test_pq, number=10000))
print(timeit.timeit(test_list, number=10000))

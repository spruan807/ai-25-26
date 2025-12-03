import heapq
from collections import defaultdict

####################### INPUT #######################
global n,m,q
n,m,q  = map(int, input().split())

##### initialize data #####
weights = [ [0]*(n+1) for x in range(n+1)]
neighbors = defaultdict(list)
queries = []
bestDistances = [ [10**10]*(n+1) for x in range(n+1) ]

for i in range(m):
    a,b,c = map(int, input().split())
    neighbors[a].append(b)
    neighbors[b].append(a)
    weights[a][b] = c
    weights[b][a] = c

for i in range(q):
    a,b = map(int, input().split())
    queries.append((a,b))

####################### GOOD PRINTING #######################
def print2d(arr):
    for r in arr:
        print(r)


####################### DIJKSTRAS #######################
def shortestRoute(a,b):
    # print(f"NOW CHECKING {a} to {b}")
    
    seen = [False] * (n+1)
    seen[a] = True
    pq = []
    heapq.heappush(pq,(0,a))

    while pq:
        currWeight, currNode = heapq.heappop(pq)
        
        
        for nb in neighbors[currNode]:
            w = weights[currNode][nb]
            newDist = w + currWeight
            
            # print(f"CURRNODE is {currNode}")
            # print(f"NEIGHBOR is {nb}")
            # print(f"seen before check: {seen}")
            # print(f"new dist before check: {newDist}")
            # print(f"prev best dist before check: {bestDistances[currNode][nb]}")
            
            if newDist < bestDistances[a][nb]:
                seen[nb] = True
                bestDistances[a][nb] = newDist
                bestDistances[nb][a] = newDist
                heapq.heappush(pq, (newDist,nb))

            
            # print(f"this is the pq after: {pq}")
            # print(f"best distances:")
            # print2d(bestDistances)
            # print(f"neighbors of {currNode}: {neighbors[currNode]}")

    ans = bestDistances[a][b]
    if ans == 10**10:
        ans = -1
    return ans

####################### OUTPUT #######################
ans = ""
for (a,b) in queries:
    shortest = str(shortestRoute(a,b))
    ans+= shortest + "\n"

print(ans)
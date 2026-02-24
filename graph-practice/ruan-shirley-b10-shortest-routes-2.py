import heapq
from collections import defaultdict

# shirley ruan

####################### INPUT #######################
global n,m,q
n,m,q  = map(int, input().split())

##### initialize data #####
weights = defaultdict(list)
neighbors = defaultdict(list)
queries = []


for i in range(m):
    a,b,c = map(int, input().split())
    neighbors[a].append(b)
    neighbors[b].append(a)
    
    if a < b:
        weights[(a,b)].append(c)
    else:
        weights[(b,a)].append(c)

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
    
    bestDistances = [ 10**10 for x in range(n+1) ]
    bestDistances[a] = 0

    seen = [False] * (n+1)
    seen[a] = True

    pq = []
    heapq.heappush(pq,(0,a))

    while pq:
        if all(seen):
            break
        currWeight, currNode = heapq.heappop(pq)
        # print(f"this is the pq after pop: {pq} \n")
        
        for nb in neighbors[currNode]:
            if all(seen):
                break

            if currNode < nb:
                ws = weights[(currNode,nb)]
            else:
                ws = weights[(nb,currNode)]

            w = min(ws)
            newDist = w + currWeight
            
            # print(f"CURRNODE is {currNode}")
            # print(f"neighbors: {neighbors[currNode]}")
            # print(f"NEIGHBOR is {nb}")
            # print(f"new dist before check: {newDist}")
            # print(f"prev best dist before check: {bestDistances[nb]}")
            
            if not seen[nb] or newDist < bestDistances[nb]:
                bestDistances[nb] = newDist
                heapq.heappush(pq, (newDist,nb))
                seen[nb] = True

            # print(f"this is the pq after push: {pq} \n")

    ans = bestDistances[b]
    if ans == 10**10:
        ans = -1
    return ans

####################### OUTPUT #######################

ans = ""
for (a,b) in queries:
    shortest = str(shortestRoute(a,b))
    ans+= shortest + "\n"

print(ans)
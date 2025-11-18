from collections import defaultdict

n,m  = map(int, input().split())

roads = []
maxSize = -1
seen = [False] * (n+1)
ans = []

for x in range(m):
    a,b = map(int, input().split())
    roads.append((a,b))

def default(val):
    return lambda: val

unionfind = defaultdict(int)
sizes = defaultdict(default(1))

for x in range(n):
    unionfind[x+1] = x+1
    sizes[x+1] = 1

def bigboss(a,b,m):
    ogboss = unionfind[b]

    while ogboss != unionfind[ogboss]:
        ogboss = unionfind[ogboss]

    while unionfind[a] != a:
        a = unionfind[a] # this won't error right...
    
    if ogboss == a:
        return m

    unionfind[b] = a
    popped = sizes.pop(ogboss,-1)

    if popped!=-1:
        sizes[a] += popped 
    else:
        sizes[a] += 1

    if sizes[a] > m:
        m = sizes[a]

    # print(f"boss is {a} and minion is {b}")
    # print(f"og boss is {ogboss}")
    # goodPrint(unionfind)
    # goodPrint(sizes)
    
    return m

def goodPrint(d): # sum the printing
    bigOlString = "{"
    for (k,v) in d.items():
        bigOlString += f"{k}:{v}, "

    print(bigOlString + "}")

for (a,b) in roads:

    if seen[a] and not seen[b]:
        maxSize = bigboss(a,b,maxSize)
    else: 
        maxSize = bigboss(b,a,maxSize)

    seen[a] = True
    seen[b] = True
    ans.append(f"{len(sizes)} {maxSize}")

out = "\n".join(ans)
print(out)
    


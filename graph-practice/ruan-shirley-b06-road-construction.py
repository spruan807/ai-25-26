

############### INITIALIZE VARIABLES ############### 

### VARIABLES PT 1 ###
roads = []
ans = []

### STRING VER ###

# stringInput = """10 20
# 9 5
# 9 6
# 5 9
# 8 10
# 5 3
# 5 2
# 10 8
# 10 7
# 5 9
# 10 9
# 10 9
# 1 5
# 9 5
# 2 10
# 10 7
# 6 9
# 10 8
# 3 1
# 10 9
# 9 2"""

# splitInput = stringInput.split("\n")
# n,m = map(int, splitInput[0].split())

# for x in splitInput[1:]:
#     a,b = map(int, x.split())
#     roads.append((a,b))

### INPUT VER ##

n,m  = map(int, input().split()) # input

for x in range(m):
    a,b = map(int, input().split()) # input ver
    roads.append((a,b))

### VARIABLES PT 2 ###
global ncomponents 
ncomponents = n

bosses = [ x for x in range(n+1) ]
sizes = [1]*(n+1)
maxSize = -1

def goodPrint(d): # sum the printing
    bigOlString = "{"
    for n in range(len(d)):
        bigOlString += f"{n}:{d[n]}, "

    print(bigOlString + "}")

def find(v):
    parent = bosses[v]
    if v == parent:
        return v
    bosses[v] = find(parent)

    return bosses[v]

def union(a,b):
    global ncomponents
    
    ap = find(a)
    bp = find(b)

    bossSize = -1

    if ap!=bp:
        ncomponents -= 1

        if sizes[ap] > sizes[bp]:
            sizes[ap] += sizes[bp]
            bosses[bp] = ap
            bossSize = sizes[ap]
        else:
            sizes[bp] += sizes[ap]
            bosses[ap] = bp
            bossSize = sizes[bp]

    # print(f"a is {a}")
    # print(f"b is {b}")
    # print(f"a boss is {ap}")
    # print(f"b boss is {bp}")
    # print(f"a size is {sizes[ap]}")
    # print(f"b size is {sizes[bp]}")
    # print(f"new boss size is {bossSize}")
    # print("bosses are")
    # goodPrint(bosses)
    # print("sizes are")
    # goodPrint(sizes)

    return bossSize

for (a,b) in roads:
    newSize = union(a,b)

    if maxSize < newSize:
        maxSize = newSize

    newline = f"{ncomponents} {maxSize}"
    ans.append(newline)

out = "\n".join(ans)
print(out)

    


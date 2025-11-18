from collections import defaultdict
import io

class Graph:
    ## INIT
    def __init__(self, es, ws, nv=0, d=False):
        self.edges = es
        self.weights = ws
        self.nvertices = nv
        self.directed = d
            
        if ~self.directed:
            self.update_undirected()
            
        if nv==0:
            self.update_nvertices()
            
        self.cleanup()
    
    ## COUNT VERTICES
    
    def update_nvertices(self):
        ans = 0
        
        if self.edges!=[]:
            ans = len(self.edges)
            
        self.nvertices = ans
        
    ## UPDATE UNDIRECTED EDGES AND WEIGHTS
    
    def update_undirected(self):
        newedges = self.edges.copy()
        newweights = self.weights.copy()
        
        for k in self.edges:
            vertices = self.edges[k]
            for v in vertices:
                newedges[v].add(k)
                newweights[(v,k)] = self.weights[(k,v)]
                
        self.edges = newedges
        self.weights = newweights
        
    ## CLEANUP
    
    def cleanup(self):
        oldKeys = set(self.edges.keys())
        newKeyPairs = { k : n for (n,k) in enumerate(oldKeys)}
        newedges = defaultdict(set)
        
        for (k,n) in newKeyPairs.items():
            vertices = self.edges[k]
            newvs = set()
            for v in vertices:
                newvs.add(newKeyPairs[v])
            newedges[n] = newvs
            
        newweights = defaultdict(int)
        
        for (x,y) in self.weights.keys():
            newKey = (newKeyPairs[x], newKeyPairs[y])
            newweights[newKey] = self.weights[(x,y)]
            
        self.edges = newedges
        self.weights = newweights
            
    
    ## READERS + HELPERS
        
    def clearcomments(s):
        nospaces = s.strip()
        #print(nospaces)
        idx = nospaces.find("#")
        ans = nospaces
        
        if idx>-1:
            ans = nospaces[0:idx]
        
        return ans
        
    @classmethod
    def reader(cls, lines, directed):
        newedges = defaultdict(set)
        newweights = defaultdict(int)
        checkweights = False
        
        for line in lines:
            if "WEIGHTS" in line:
                checkweights = True
                continue
            
            clear = Graph.clearcomments(line)    
            
            if len(clear)==0:
                continue
                
            if checkweights:
                nums = [int(x) for x in clear.split()] # or map
                x = nums[0]
                y = nums[1]
                w = nums[2]
                newweights[(x,y)] = w
            else: 
                nums = [int(x) for x in clear.split()] # or map
                edges = set(nums[1:])
                vertex = nums[0]
                newedges[vertex] = edges
    
        ans = Graph(newedges, newweights, d=directed)
        return ans
        
    def dfs(self):
        seen  = [False] * self.nvertices
        
        entries = [0] * self.nvertices
        exits = [0] * self.nvertices
        parents = [0] * self.nvertices
        ras = [0] * self.nvertices
        
        firstjob = 0
        seen[firstjob] = True
        
        def dfs_h(t,v):
            time = t
            entries[v] = time
            currRA = v
            
            for n in self.edges[v]:
                if not seen[n]:
                    seen[n] = True
                    parents[n] = v
                    (t,r) = dfs_h(time+1,n)
                    time = t
                    if entries[currRA] > entries[r]:
                        currRA = r
                elif n is not parents[v]:
                    compRA = ras[n]
                    if entries[currRA] > entries[compRA]:
                        currRA = compRA
                    
                    
            exits[v] = time+1
            ras[v] = currRA
            
            return (time+1, currRA)
        
        dfs_h(0,firstjob)
        
        return {"entries" : entries, "exits" : exits, "parents" : parents, "ras" : ras}
    
    # 5-8 write-up
    
    def matrix_to_list(m):
        ans = defaultdict(list)                       
        lenny = len(m)                   
        for a in range(lenny):            
            for b in range(lenny):       
                if m[a][b] == 1:        
                    ans[a].append(b)     
        return ans
    
    def count_edges(adjList):
        ans = 0
        for k in adjList.keys():
            for v in adjList[k]:
                if v > k:
                    ans+=1
                    
        return ans
    
    def list_to_inc_matrix(a):
        lenny = len(a)      
        
        numEdges = Graph.count_edges(a)
    
        ans = [ [0 for x in range(numEdges)] for x in range(lenny)] 
        
        count = 0
    
        for k in a.keys():
            for v in a[k]:
                if v > k:
                    ans[v][count] = 1
                    ans[k][count] = 1
                    count+=1
                
        return ans                          
    
    def inc_matrix_to_list(m):
        ans =  defaultdict(list)            # answer is an adjacency list
        nVertices = len(m)                       # the incidence matrix is a rectangle by definition 
        nEdges = len(m[0])
    
        for e in range(nEdges):          # for each edge
            fst = -1                        # initialize a first and second value for the  
            snd = -1                        # eventual values that will be added to the adjacency list
            for v in range(nVertices):      # for each vertex of the edge
                if m[v][e] == 1:            
                    if fst==-1:             # update first if empty
                        fst = v
                    else:
                        snd = v             # update second if first is done
    
            ans[fst].append(snd)
            ans[snd].append(fst)
    
        return ans
        
    @classmethod
    def file_reader(cls, openfile, directed=False):
        with open(openfile) as f:
            lines = f.readlines() # array with all the lines in the file
            
        ans = Graph.reader(lines, directed)
        return ans
        
    @classmethod
    def string_reader(cls, str, directed=False):
        fakefile = io.StringIO(str)
        lines = fakefile.readlines()
        
        ans = Graph.reader(lines, directed)
        return ans

    ## REPR
    def __repr__(self):
        return f"[Graph, \nV={self.nvertices}, \nE={self.edges}, \nW={self.weights}]"
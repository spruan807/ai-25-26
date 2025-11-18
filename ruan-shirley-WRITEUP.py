# shirley ruan
# 5-8 writeup
# rewrite ver. 
# 10/15/25


# QUESTION: Present correct and eﬃcient algorithms to convert an 
# undirected graph G between the following graph data structures. 
# You must give the time complexity of each algorithm, 
# assuming n vertices and m edges.

# the following code was written within the Graph class. 

# DEFINITIONS:
# adjacency matrix: an n by n array where each row and column represents a vertex.
#                   elements of 1 indicate edges, while 0 indicates no edge.
#                   
#                   for example, if the element in the second row and fourth
#                   column is 1 (if adjmatrix[1][3]==1), then the 
#                   the second vertex and the fourth vertex share an edge. 
#
# adjacency list: a collection matching each vertex to a list of their neighbors.
#                 in our implementation, an adjacency list is represented as
#                 a dictionary (defaultdict), with vertices as keys 
#                 and lists of connected vertices as values. 
#
#                 for example,
#                 key 0 with value [1,3] represents vertex 0 that is connected
#                 to vertices 1 and 3. 
#
# incidence matrix: an n by m array where each row represents a vertex and 
#                   each column represents an edge. for an undirected graph,
#                   each column m lists 1 in the nth row to indicate 
#                   that the nth vertex is an endpoint of the mth edge. 
#                   we use 0 for no relation. as a result, each column is 
#                   composed of a bunch of 0s and two 1s (two endpoints).
#                   
#                   for example, if the first row has 1 in the second column, 
#                   then the second edge has the first vertex as an endpoint. 
#                   the second column may another 1 in the fourth row. the 
#                   fourth vertex is thus the other endpoint of the second edge/
#                   

########################### PART A ###########################
# QUESTION: Convert from an adjacency matrix to adjacency lists.

# My solution iterates through each element of the adjacency matrix. 
#
# STEP 1: Since the matrix is n by n, we must use a nested for loop
#         over range n to access all elements. Say the first for loop checks for row a
#         from 0 to n, and the second for loop checks for column b from 0 to n. 
#         Within the second loop, check for edges. 
# STEP 2: If row a and column b share an edge, I add b to the ath key list in 
#         my answer adjacency list. 
#
# As the for loop iterates through all a and b, the answer adjacency list 
# fills with all edges indicated in the adjacency matrix. 
#
# This is an n^2 algorithm due to the nested for loop that iterates
# through each vertex for each vertex. 

def matrix_to_list(m):
        ans = defaultdict(list)                       
        lenny = len(m)                   
        for a in range(lenny):            
            for b in range(lenny):       
                if m[a][b] == 1:        
                    ans[a].append(b)     
        return ans
    
########################### PART B ###########################
# QUESTION: Convert from an adjacency list to an incidence matrix. 
# An incidence matrix M has a row for each vertex and a column for each edge, 
# such that M [i, j] = 1 if vertex i is part of edge j, otherwise M [i, j] = 0.

# Begin by counting all the edges in the adjacency list.
# STEP 1: Check each vertex v in each key k in the adjacency list.If v>k, 
#         increment the edge counter. 
#         This condition ensures that we don't double count edges (see note 
#         below for why we should not double count). 
#         This implementation also assumes that we don't have self edges.

# Now, we can start filling the incidence matrix. 
# STEP 2: After counting m edges, fill a 2D array with n rows and m columns with 0s. 
#         This is the initial answer incidence matrix. 
# STEP 3: To fill the matrix with 1s for our final answer, we can use a nested for loop 
#         and counter again. Say the counter variable is c. 
# STEP 4: For each edge in the adjacency list (with endpoints k and v), if v>k, 
#         update rows k and v with 1 in the cth column. In the output 
#         incidence matrix, this marks k and v as endpoints of edge c. 
# STEP 5: Increment c. 
#
# As the for loop iterates through the adjacency list, the two rows representing 
# the endpoints of the cth edge are updated in the incidence matrix. 
#
# Due to the nested for loop that iterates through each edge
# twice (since it's undirected) for each vertex, 
# this is an (2nm) algorithm   
#
# COUNTING NOTE: Although the graph is undirected, I do not count the edge 
# between 1 and 3 and the edge between 3 and 1 as two separate edges. 
# The incidence matrix uses signs (+ or -) to indicate directed edges, 
# but it does not distinguish for undirected edges. Thus, avoiding the 
# double counting simply gets rid of duplicate edge columns in the final 
# incidence matrix. 
    
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
    
########################### PART C ###########################
# QUESTION: Convert from an incidence matrix to adjacency lists.
#
# Similar to the previous questions, we must iterate through all elements 
# of the input matrix with a nested for loop. 
# 
# STEP 1: Find the numbers of vertices n and edges m by taking the length 
#         of the input array and the length of the first row. Since 
#         incidence matrices are rectangular by definition (each vertex/row 
#         is filled with 0s and 1s for each edge/column), taking the length 
#         of only the first row works. 
# STEP 2: For each edge/column in the input matrix, initialize two variables 
#         fst and snd.
# STEP 3: For each vertex/row in the input matrix, update fst and snd with the 
#         two endpoint vertices in the edge/column (so when you find 1 in the 
#         edge/column, update fst or snd). 
# STEP 4: Using a defaultdict to represent the output adjacency list, fst and snd
#         can be used as keys to represent their respective vertices. Add snd 
#         as a neighbor in the fst vertex key. Add fst as a neighbor for the 
#         snd key as well. 
#
# As the for loops iterate through each edge in the incidence matrix, the
# output adjacency list fills with all vertices and their neighbor lists. 
#
# This algorithm is also an nm algo due to the nested for loop,
# but since the incidence matrix doesn't list undirected edges 
# twice, we don't iterate over each edge twice, getting rid of
# the 2 in the 2nm from the previous question.
    
    def inc_matrix_to_list(m):
        ans =  defaultdict(list)            
        nVertices = len(m)                        
        nEdges = len(m[0])
    
        for e in range(nEdges):          
            fst = -1                         
            snd = -1                        
            for v in range(nVertices):      
                if m[v][e] == 1:            
                    if fst==-1:             
                        fst = v
                    else:
                        snd = v             
    
            ans[fst].append(snd)
            ans[snd].append(fst)
    
        return ans
        
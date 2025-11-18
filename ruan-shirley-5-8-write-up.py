# 5-8 write-up

def adj_matrix_to_list(m):
    ans = []                         # answer is adjacency list
    lenny = len(m)                   # matrix has every vertex as rows and cols
    for a in range(lenny):           # for every row and col in the matrix, 
        for b in range(lenny):       
            if m[a][b] == 1:         # if the cell contains 1, then the row vertex and col vertex have an edge
                ans.append((a,b))    # add the edge to the adjacency list
    return ans

def adj_list_to_inc_matrix(a):
    lenny = len(ans)      

    ans = [ [0 for x in range(lenny)] for x in range(lenny)] # answer is an incidence matrix, initialized with 0s so it's "empty"
    count = 0                           # this will keep track of which edge (col in matrix) we're on

    for curr in a:                      # for each edge in the adjacency list 
        x,y = curr                      # extract the vertices from the current tuple in the adjacency list

        ans[x][count] = 1               # mark the vertex as being an endpoint of the (count)th edge
        ans[y][count] = 1               # same with the other vertex

        count+=1                        # increment the count
            
    return ans                          

def inc_matrix_to_adj_list(m):
    ans = []                            # answer is an adjacency list
    rows = len(m)                       # the incidence matrix is a rectangle by definition 
    cols = len(m[0])

    for c in range(cols):               # for each edge
        fst = -1                        # initialize a first and second value for the  
        snd = -1                        # eventual tuple that will be added to the adjacency list
        for r in range(rows):           # for each vertex of the edge
            if m[r][c] == 1:            
                if fst==-1:             # update first if empty
                    fst = r
                else:
                    snd = r             # update second if first is done

            ans.append((fst, snd))      # add the tuple to the adjacency list

    return ans
                
            
        
    

            
        
            

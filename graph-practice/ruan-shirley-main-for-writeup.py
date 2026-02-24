from collections import defaultdict, deque
from graph import Graph


def main():
    # graph is 
    #     0 
    #   1   3
    #  2 4    5
    exmat = [ [ 0,1,0,1,0,0 ], 
              [ 1,0,1,0,1,0 ], 
              [ 0,1,0,0,0,0 ], 
              [ 1,0,0,0,0,1 ],
              [ 0,1,0,0,0,0 ],
              [ 0,0,0,1,0,0 ] ]
    exlist = { 0:[1,3], 1:[0,2,4], 2:[1], 3:[0,5], 4:[1], 5:[3] }
    exincmat = [    [1,1,0,0,0],
                    [1,0,1,1,0],
                    [0,0,1,0,0],
                    [0,1,0,0,1],
                    [0,0,0,1,0],
                    [0,0,0,0,1]     ]
              
    t1 = Graph.matrix_to_list(exmat)
    print("now testing adjacency matrix to list:\n")
    for key in t1.keys():
        print(f"{key} : {t1[key]}")
    
    t2 = Graph.list_to_inc_matrix(exlist)
    print("\nnow testing adjacency list to incidence matrix\n")
    for vertex in t2:
        print(vertex)
       
    t3 = Graph.inc_matrix_to_list(exincmat)
    print("\nnow testing incidence matrix to adjacency list\n")
    for key in t3.keys():
        print(f"{key} : {t3[key]}")
    
main()
import pygame
import pytest
from collections import deque

class Board:
    def __init__(self):
        self.grid = []
        self.currH = 0 # current heuristic
        self.numMoves = 0
        self.pastMoves = deque() 
        self.futureMoves = deque() 

        self.reset()

    def move(dir):
        # takes in a direction
        # modifies the grid array, currH, and pastMoves to make that move
        # increments numMoves
        pass
    
    def reset():
        # generates new game board
        pass

    def undo():
        pass

    def redo():
        pass

class Strat:
    def lookAhead(b):
        # ngl what is this for
        pass

    def legalMoves(b):
        pass

    def mergeHeuristic():
        # write it
        pass
    

class Vis:
    def drawRecMoves(startX, startY, endX, endY):
        # helper for drawUI
        # draws recommended moves in mini boards above the main board
        # in order of: up down left right
        # highlight the best(s)
        # returns
        pass

    def drawExtraData(startX, startY, endX, endY):
        # helper for drawUI
        # disp curr number of moves, curr heuristic, move history below main board
        pass

    def drawBoard(startX, startY, endX, endY):
        # helper for drawUI
        # draws the game board
        pass

    def drawUI():
        # combines helpers above
        pass

class Test:
    def rep(n):
        pass

class Controls:
    def run():
        # runs the visualization, processing key events
        # History mechanism so you can move backwards and forwards in the list of moves already seen.
        # Computer single play using “a”.
        # Computer continuous play (forward/backward) using “f”/“b”.
        # Pause/resume the animation hitting the space bar.
        # You can take over play from the point the animation is stopped. (Is this a useful feature?)

        pass
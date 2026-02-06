import pygame
import pytest
from collections import deque

class Board:
    def __init__(self):
        self.grid = []
        self.currH = 0 # current heuristic
        self.numMoves = 0
        self.pastMoves = deque() # deque of (moveInt, boardList)
        self.futureMoves = deque() # uhhhhh rethink this

    def move(dir):
        pass

    def undo():
        pass

    def  redo():
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
        # disp curr number of moves, curr heuristic below main board
        pass

    def drawBoard(startX, startY, endX, endY):
        # helper for drawUI
        # draws the game board
        pass

    def drawUI():
        # combines helpers above
        pass

class Test:
    # what it says on the tin 
    def rep(n):
        pass






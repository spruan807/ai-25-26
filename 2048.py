import pygame
# import pytest
from collections import deque
import random
import copy

# fix the recmoves so that it dont recalculate every single time
# add heuristic w/ recommended boards showing heuristic
# fix board to work with new Move class

# number colors
colors = {
    0: (205, 193, 180), 
    2: (238, 228, 218), 
    4: (245, 224, 200),
    8: (242, 177, 121), 
    16: (245, 149, 99), 
    32: (246, 124, 95),
    64: (246, 94, 59), 
    128: (237, 207, 114), 
    256: (237, 204, 97),
    512: (237, 200, 80), 
    1024: (237, 197, 63), 
    2048: (237, 194, 46)
}

textColor = (119, 110, 101)
bgColor = (187, 173, 160)
tick = 150 # milliseconds

class Board:
    #################### INIT ####################
    def __init__(self):
        self.grid = [] #1d array
        self.currH = 0 
        self.numMoves = 0
        self.pastMoves = deque() # stores (move, grid, currH)
        self.futureMoves = deque() # stores (move, grid, currH) for redo
        self.recMoves = [] # stores recommended moves
        
        # animation data: list of dicts {'val': int, 'from': (r, c), 'to': (r, c)}
        self.animations = [] 
        self.lastMoveTime = 0
        self.dead = False

        self.reset()
        
    def reset(self):
        # CHANGED: 1D List initialization
        self.grid = [0] * 16
        self.currH = 0
        self.numMoves = 0
        self.pastMoves.clear()
        self.futureMoves.clear()
        self.animations = []
        self.dead = False
        self.spawnTile()
        self.spawnTile()
    
        (death, moves) = Move.legalMoves(self)
        self.recMoves = moves
        
        
    #################### TILE SPAWNING ####################
    def getEmptyCells(self):
        # returns 2d coordinates of all empty tiles
        return [(i // 4, i % 4) for i, val in enumerate(self.grid) if val == 0]

    def spawnTile(self):
        empty = self.getEmptyCells()
        
        if empty:
            r, c = random.choice(empty)
            val = 4 if random.random() > 0.9 else 2
            
            # CHANGED: Access grid via linear index
            self.grid[r * 4 + c] = val
            
            # Add spawn animation (appearing in place)
            self.animations.append({'val': val, 'from': (r, c), 'to': (r, c), 'type': 'spawn'})
        
    
#################### UNDO/REDO ####################

    def undo(self):
        if not self.pastMoves:
            return
        
        moveDir, prevGrid, prevScore = self.pastMoves.pop()
        
        # Push to future
        self.futureMoves.append((moveDir, copy.deepcopy(self.grid), self.currH))
        
        self.grid = prevGrid
        self.currH = prevScore
        self.numMoves -= 1
        self.animations = [] # Disable animation on undo

    def redo(self):
        if not self.futureMoves:
            return

        moveDir, nextGrid, nextScore = self.futureMoves.pop()
        
        # Save current to past
        self.pastMoves.append((moveDir, copy.deepcopy(self.grid), self.currH))
        
        self.grid = nextGrid
        self.currH = nextScore
        self.numMoves += 1
        self.animations = [] # Disable animation on redo
        
    def __repr__(self):
        return str(self.grid)

class Move:
    #################### MOVES ####################
    def mergeRowLeft(board, row, rowIndex):
        # Returns: newRow, scoreAdd, rowAnimations
        # rowAnimations is list of {'val': v, 'from_idx': c_old, 'to_idx': c_new}
        
        nonZero = [(r, i) for i, r in enumerate(row) if r != 0] # (value, original_index)
        newRow = []
        animations = []
        scoreAdd = 0
        skip = False
        
        writeIdx = 0
        i = 0
        while i < len(nonZero):
            val, originalIdx = nonZero[i]
            
            if i + 1 < len(nonZero) and nonZero[i+1][0] == val:
                # Merge
                mergedVal = val * 2
                newRow.append(mergedVal)
                scoreAdd += mergedVal
                
                # Record movements for both tiles merging
                animations.append({'val': val, 'from_idx': originalIdx, 'to_idx': writeIdx})
                animations.append({'val': nonZero[i+1][0], 'from_idx': nonZero[i+1][1], 'to_idx': writeIdx})
                
                i += 2
                writeIdx += 1
            else:
                # No Merge
                newRow.append(val)
                animations.append({'val': val, 'from_idx': originalIdx, 'to_idx': writeIdx})
                i += 1
                writeIdx += 1
        
        while len(newRow) < 4:
            newRow.append(0)
            
        return newRow, scoreAdd, animations

    def moveGrid(board, dir):
        oldGrid = copy.deepcopy(board.grid)
        newScore = board.currH
        changed = False
        newGrid = []
        
        board.animations = [] # Clear previous animations
        
        # conversion to 2d BAD PLEASE FIX
        workingGrid = []
        for r in range(4):
            start = r * 4
            workingGrid.append(board.grid[start : start + 4])
        
        # transform grid to "Left" orientation
        # 0: Up (Transpose), 1: Down (Transpose+Flip), 2: Left (None), 3: Right (Flip)
        if dir == 0:
            workingGrid = [list(row) for row in zip(*workingGrid)]
        elif dir == 1:
            workingGrid = [list(row) for row in zip(*workingGrid)]
            workingGrid = [row[::-1] for row in workingGrid]
        elif dir == 3:
            workingGrid = [row[::-1] for row in workingGrid]

        # process rows
        for r, row in enumerate(workingGrid):
            mergedRow, pts, rowAnims = Move.mergeRowLeft(board, row, r)
            newGrid.append(mergedRow)
            newScore += pts
            
            if mergedRow != row:
                changed = True
                
            # Convert relative row indices back to absolute grid coordinates for animation
            for anim in rowAnims:
                cOld = anim['from_idx']
                cNew = anim['to_idx']
                
                # Map (r, c) based on orientation
                if dir == 0: # Up
                    start = (cOld, r)
                    end = (cNew, r)
                elif dir == 1: # Down
                    start = (3 - cOld, r)
                    end = (3 - cNew, r)
                elif dir == 2: # Left
                    start = (r, cOld)
                    end = (r, cNew)
                elif dir == 3: # Right
                    start = (r, 3 - cOld)
                    end = (r, 3 - cNew)
                    
                board.animations.append({
                    'val': anim['val'],
                    'from': start,
                    'to': end,
                    'type': 'move'
                })

        # restore orientation
        if dir == 0:
            newGrid = [list(row) for row in zip(*newGrid)]
        elif dir == 1:
            newGrid = [row[::-1] for row in newGrid]
            newGrid = [list(row) for row in zip(*newGrid)]
        elif dir == 3:
            newGrid = [row[::-1] for row in newGrid]
            
        return (changed, oldGrid, newGrid, newScore)
    
    def moveData(board, data):
        (changed, oldGrid, newGrid, newScore) = data
        
        if changed:
            # store in pastMoves: (move, grid_before, score_before)
            board.pastMoves.append((dir, oldGrid, board.currH))
            board.futureMoves.clear()
            
            # flatten 2D 
            board.grid = [val for row in newGrid for val in row]
            
            board.currH = newScore
            board.numMoves += 1
            return True
        
        board.animations = [] # Reset animations if no move occurred
        return False
    
    def legalMoves(board):
        ans = [(False, None) for x in range(4)]
        death = True
        
        for dir in range(4):
            tempBoard = copy.deepcopy(board)
            data = Move.moveGrid(tempBoard, dir)
            changed = Move.moveData(tempBoard, data)
            
            if changed:
                ans[dir] = (True, tempBoard)
                death = death and not changed
        
        return (death, ans)
    
    def move(board, dir):
        # dir: 0=Up, 1=Down, 2=Left, 3=Right
        
        (changed, newBoard) = board.recMoves[dir]
        
        if changed:
            newBoard.spawnTile()
            (death, moves) = Move.legalMoves(newBoard)
            
            if death:
                newBoard.dead = True
            
            newBoard.recMoves = moves
            newBoard.lastMoveTime = pygame.time.get_ticks()
            
            return newBoard
        
        return board

class Strat:
    def lookAhead(b):
        # ngl what is this for
        pass

    def randomPlay(b):
        randDir = random.randint(0,3)
        return Move.move(b, randDir)
        
    def mergeHeuristic(b):
        # write it
        pass
    
class Vis:
    def __init__(self, board):
        self.board = board
        if not pygame.font.get_init():
            pygame.font.init()
        self.font = pygame.font.Font(None, 40)
        self.smallFont = pygame.font.Font(None, 24)

    def drawRecMoves(self, screen, startX, startY, endX, endY):
        
        width = endX - startX
        miniSize = width // 4 - 10 # Size of one mini board, fit 4 in a row
        
        labels = ["up", "down", "left", "right"]
        
        # init positions
        mx = startX 
        my = startY + 30
        
        # legal moves
        legal = self.board.recMoves
        
        for i in range(4):
            (moved, tempBoard) = legal[i]
            
            # Calculate position for this mini board
            mx = startX + i * (miniSize + 10) + 5
            
            # Draw Label
            labelSurf = self.smallFont.render(labels[i], True, textColor)
            labelRect = labelSurf.get_rect(center=(mx + miniSize/2, my - 10))
            screen.blit(labelSurf, labelRect)

            # Draw background for mini board
            pygame.draw.rect(screen, bgColor, (mx, my, miniSize, miniSize))

            if not moved:
                # Draw visual indicator for invalid move
                pygame.draw.line(screen, (100,100,100), (mx, my), (mx+miniSize, my+miniSize), 2)
                pygame.draw.line(screen, (100,100,100), (mx+miniSize, my), (mx, my+miniSize), 2)
            else:
                # Draw Mini Board content
                cellW = miniSize / 4
                for r in range(4):
                    for c in range(4):
                        # CHANGED: Access flat list [r*4 + c]
                        val = tempBoard.grid[r * 4 + c]
                        if val != 0:
                            color = colors.get(val, colors[2048])
                            rect = pygame.Rect(mx + c*cellW, my + r*cellW, cellW - 1, cellW - 1)
                            pygame.draw.rect(screen, color, rect)

    def drawExtraData(self, screen, startX, startY, endX, endY):
        # Data displayed BELOW the main board
        pad = 20
        yOffset = startY
        
        stats = [
            f"score: {self.board.currH}",
            f"moves: {self.board.numMoves}"
        ]
        
        # Display Stats horizontally if space permits, or vertical list
        statText = " | ".join(stats)
        sSurf = self.font.render(statText, True, textColor)
        screen.blit(sSurf, (startX, yOffset))
        
        controls = [
            "arrow keys to move",
            "(u)ndo | (r)edo | (n)ew game"
        ]
        
        yOffset += 40
        for line in controls:
            cSurf = self.smallFont.render(line, True, textColor)
            screen.blit(cSurf, (startX, yOffset))
            yOffset += 25

    def drawBoard(self, screen, startX, startY, endX, endY):
        # Draw background container
        rect = pygame.Rect(startX, startY, endX - startX, endY - startY)
        pygame.draw.rect(screen, bgColor, rect)
        
        width = endX - startX
        cellSize = width // 4
        padding = 10

        # Check animation status
        now = pygame.time.get_ticks()
        dt = now - self.board.lastMoveTime
        isAnimating = dt < tick and len(self.board.animations) > 0
        
        if isAnimating:
            # INTERPOLATION DRAWING
            # 1. Draw empty grid slots first (backgrounds of cells)
            for r in range(4):
                for c in range(4):
                    cx = startX + c * cellSize + padding
                    cy = startY + r * cellSize + padding
                    cw = cellSize - 2 * padding
                    pygame.draw.rect(screen, colors[0], (cx, cy, cw, cw), border_radius=5)
            
            # 2. Draw moving tiles
            progress = dt / tick # 0.0 to 1.0
            
            for anim in self.board.animations:
                val = anim['val']
                r1, c1 = anim['from']
                r2, c2 = anim['to']
                
                # Lerp coordinates
                currR = r1 + (r2 - r1) * progress
                currC = c1 + (c2 - c1) * progress
                
                cx = startX + currC * cellSize + padding
                cy = startY + currR * cellSize + padding
                cw = cellSize - 2 * padding
                
                if anim.get('type') == 'spawn':
                    continue

                self._drawTile(screen, val, cx, cy, cw)
            
            # 3. Draw spawning tiles
            if progress > 0.8:
                for anim in self.board.animations:
                    if anim.get('type') == 'spawn':
                         r, c = anim['to']
                         cx = startX + c * cellSize + padding
                         cy = startY + r * cellSize + padding
                         cw = cellSize - 2 * padding
                         self._drawTile(screen, anim['val'], cx, cy, cw)

        else:
            # STATIC DRAWING (Standard)
            for r in range(4):
                for c in range(4):
                    # CHANGED: Access flat list [r*4 + c]
                    val = self.board.grid[r * 4 + c]
                    cx = startX + c * cellSize + padding
                    cy = startY + r * cellSize + padding
                    cw = cellSize - 2 * padding
                    
                    # Draw base empty cell color behind everything
                    pygame.draw.rect(screen, colors[0], (cx, cy, cw, cw), border_radius=5)
                    
                    if val != 0:
                        self._drawTile(screen, val, cx, cy, cw)

    def _drawTile(self, screen, val, x, y, size):
        color = colors.get(val, colors[2048])
        pygame.draw.rect(screen, color, (x, y, size, size), border_radius=5)
        
        textColor = (119, 110, 101) if val <= 4 else (249, 246, 242)
        fontSize = 55 if val < 100 else (45 if val < 1000 else 35)
        font = pygame.font.Font(None, fontSize)
        
        textSurf = font.render(str(val), True, textColor)
        textRect = textSurf.get_rect(center=(x + size/2, y + size/2))
        screen.blit(textSurf, textRect)

    def drawUI(self, screen):
        w, h = screen.get_size()
        
        # Dimensions
        boardSize = 350
        boardX = (w - boardSize) // 2
        boardY = (h - boardSize) // 2
        
        # 1. Recommended Moves (Top)
        # Height allocated: boardY (space above board)
        self.drawRecMoves(screen, boardX, 0, boardX + boardSize, boardY)
        
        # 2. Main Board (Center)
        self.drawBoard(screen, boardX, boardY, boardX + boardSize, boardY + boardSize)
        
        # 3. Extra Data (Bottom)
        self.drawExtraData(screen, boardX, boardY + boardSize + 20, boardX + boardSize, h)
        
        if self.board.dead:
            deathFont = pygame.font.Font(None, 100)
            deathText = deathFont.render("dead", True, textColor, bgColor)
            screen.blit(deathText, deathText.get_rect(center=(w/2, h/2)))
        
class Test:
    def __init__(self):
        pass
    def rep(n):
        pass

class Controls:
    def findStrat(id, b):
        if id==1: 
            return Strat.randomPlay(b)
        return b
    
    def manualMove(k, b):
        if k == pygame.K_UP:
            b = Move.move(b,0)
        elif k == pygame.K_DOWN:
            b = Move.move(b,1)
        elif k == pygame.K_LEFT:
            b = Move.move(b,2)
        elif k == pygame.K_RIGHT:
            b = Move.move(b,3)
        elif k == pygame.K_u: # Undo
            b.undo()
        elif k == pygame.K_r: # Redo
            b.redo()
        elif k == pygame.K_n: # New Game
            b.reset()
            
        return b
    
    def run():
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("2048 Visualization")
        clock = pygame.time.Clock()
        
        board = Board()
        vis = Vis(board)
        
        running = True
        currStrat = 0
        spamming = False
        
        while running:
            screen.fill((250, 248, 239)) # Off-white background
            
            # Event Handling
            for event in pygame.event.get():
                if board.dead:
                    continue
                elif event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_0: # on/off spam
                        spamming = not spamming
                    elif event.key == pygame.K_1: # randomPlay 
                        currStrat = 1
                    else:
                        board = Controls.manualMove(event.key, board)
            
            if spamming:
                board = Controls.findStrat(currStrat, board)
                
            vis.board = board
            
            # Draw
            vis.drawUI(screen)
            
            pygame.display.flip()
            clock.tick(200) # 60 FPS
        pygame.quit()
        
Controls.run()
from __future__ import annotations

import sys
import time
from enum import Enum

IS_WINDOWS = sys.platform == "win32"

if IS_WINDOWS:
    import msvcrt
else:
    import atexit
    import os
    import select
    import termios
    import tty
    from collections import deque

def clear_console():
    print("\033[2J\033[H", end="")

class CellType(Enum):
    EMPTY = 1,
    BALL = 2,
    PLATFORM = 3

def createGameGrid(width : int, height : int) -> list[list[CellType]]:
    grid : list[list[bool]] = []

    for x in range(width):
        row : list[bool] = []
        for y in range(height):
            row.append(CellType.EMPTY)
        grid.append(row)

    return grid

def renderGrid(grid: list[list[CellType]]) -> str: 
    finalOutput : str = ""
    # Adds - line
    finalOutput += getTopLine(grid)

    for x in grid:
        output = ""
        for gridValue in x:
            if gridValue == CellType.BALL:
                output += " o "
            elif gridValue == CellType.PLATFORM:
                output += " | "
            elif gridValue == CellType.EMPTY:
                output += "   "

        output += "\n"
        finalOutput += output

    finalOutput += getTopLine(grid)

    print(finalOutput)

def getTopLine(grid: list[list[CellType]]) -> str:
    finalOutput = ""
    for y in grid[0]:
        finalOutput += "---"
    finalOutput += "\n"
    return finalOutput

"""
Assuming speed is max in range (-1,1)
"""
def updateBall(grid: list[list[CellType]], previousPosition : list[int, int], speed : list[int, int]) -> tuple[list[list[CellType]], list[int, int], list[int, int], Winstate]:
    grid[previousPosition[0]][previousPosition[1]] = CellType.EMPTY
    width = len(grid)
    height = len(grid[0])
    
    xPosition = previousPosition[0] + speed[0]
    yPosition = previousPosition[1] + speed[1]

    #Update speed
    #Reflect at the boundary CELL itself (width-1 / height-1), not one step past it.
    #Otherwise the ball lands on the goal line, sits there for a tick drawn over the
    #paddle, and next tick clears the paddle cell and scores through it.
    if(xPosition >= width - 1):
        speed[0] = speed[0] * (-1)
    if(xPosition <= 0):
        speed[0] = speed[0] * (-1)
    if(yPosition >= height - 1):
        speed[1] = speed[1] * (-1)
    if(yPosition <= 0):
        speed[1] = speed[1] * (-1)

    #Make sure position is in boundaries
    xPosition = min(xPosition, width-1)
    xPosition = max(xPosition, 0)
    yPosition = min(yPosition, height-1)
    yPosition = max(yPosition, 0)

    winstate = Winstate.PLAYING
    #Goals are at the ends of each row -> index 1 (yPosition). index 0 (xPosition) is the
    #top/bottom wall, which is why the win was firing on the wrong axis.
    #grid[previousPosition] was just cleared, but the paddle sits in a different cell,
    #so reading it here still sees PLATFORM.
    #Player A defends column 0, so the ball getting past it means Player A loses
    if yPosition == 0:
        if grid[xPosition][yPosition] != CellType.PLATFORM:
            winstate = Winstate.BWON
    #Player B defends the last column, so the ball getting past it means Player B loses
    elif yPosition == len(grid[0])-1:
        if grid[xPosition][yPosition] != CellType.PLATFORM:
            winstate = Winstate.AWON

    grid[xPosition][yPosition] = CellType.BALL

    return (grid, (xPosition, yPosition), speed, winstate)


"""
Positions are in first column and last
"""
def updatePlatforms(grid: list[list[CellType]], playerInputs : tuple[Direction, Direction], platformSize : int, previousPositions : list[int, int]) -> tuple[list[list[CellType]],  list[int, int]]:
    #Clear player platforms
    for x in grid:
        x[0] = CellType.EMPTY
        x[len(x)-1] = CellType.EMPTY

    positionPlayerA = previousPositions[0]
    positionPlayerB = previousPositions[1]

    #Add position by 1
    if(playerInputs[0] == Direction.UP):
        positionPlayerA += 2
    elif(playerInputs[0] == Direction.DOWN):
        positionPlayerA -= 2
    if(playerInputs[1] == Direction.UP):
        positionPlayerB += 2
    elif(playerInputs[1] == Direction.DOWN):
        positionPlayerB -= 2

    #Check that the position is inside grid
    positionPlayerA = min(positionPlayerA, len(grid) - 1)
    positionPlayerA = max(positionPlayerA, 0)

    positionPlayerB = min(positionPlayerB, len(grid) - 1)
    positionPlayerB = max(positionPlayerB, 0)

    #Update platforms inside
    for i in range(len(grid)):
        if i <= positionPlayerA + int(platformSize/2) and  i >= positionPlayerA - int(platformSize/2):
            grid[i][0] = CellType.PLATFORM
    for i in range(len(grid)):
        if i <= positionPlayerB + int(platformSize/2) and  i >= positionPlayerB - int(platformSize/2):
            grid[i][len(grid[i]) - 1] = CellType.PLATFORM

    return (grid, (positionPlayerA, positionPlayerB))


class Direction(Enum):
    UP=1,
    DOWN=2,
    NONE=3

class Winstate(Enum):
    AWON=1,
    BWON=2,
    PLAYING=3

if IS_WINDOWS:
    def kbhit() -> bool:
        return bool(msvcrt.kbhit())

    def getch() -> bytes:
        return msvcrt.getch()
else:
    _savedTermios = None
    _pendingBytes = deque()

    def _enableCbreak():
        global _savedTermios
        if _savedTermios is not None or not sys.stdin.isatty():
            return
        _savedTermios = termios.tcgetattr(sys.stdin)
        atexit.register(_disableCbreak)
        tty.setcbreak(sys.stdin.fileno())

    def _disableCbreak():
        global _savedTermios
        if _savedTermios is not None:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, _savedTermios)
            _savedTermios = None

    def _readByte(timeout : float) -> bytes:
        # b"" when nothing arrives within timeout seconds
        if not select.select([sys.stdin], [], [], timeout)[0]:
            return b""
        return os.read(sys.stdin.fileno(), 1)

    def kbhit() -> bool:
        _enableCbreak()
        if _pendingBytes:
            return True
        return bool(select.select([sys.stdin], [], [], 0)[0])

    def getch() -> bytes:
        if _pendingBytes:
            return _pendingBytes.popleft()

        key = _readByte(1.0)
        if key != b'\x1b':
            return key

        # Escape starts a sequence, give the rest of it a moment to arrive
        if _readByte(0.05) != b'[':
            return b'\x1b'

        key = _readByte(0.05)
        if key == b'A':          # Arrow up
            _pendingBytes.append(b'H')
            return b'\xe0'
        elif key == b'B':        # Arrow down
            _pendingBytes.append(b'P')
            return b'\xe0'
        return b'\x1b'

def getInput() -> tuple[Direction, Direction]:
    playerA = Direction.NONE
    playerB = Direction.NONE

    if kbhit():
        key = getch()

        # Player A: W / S
        if key == b'w':
            playerA = Direction.DOWN
        elif key == b's':
            playerA = Direction.UP

        # Player B: arrow keys
        elif key == b'\xe0':
            key = getch()

            if key == b'H':
                playerB = Direction.DOWN
            elif key == b'P':
                playerB = Direction.UP

    return playerA, playerB

def runGame(fps : float):
    while(True):
        width : int = 15
        height : int = 30
        platformSize : int = 5
        playerPositions : list[int, int] = [3,3]

        grid : list[list[CellType]] = createGameGrid(width, height)
        ballPosition : list[int, int] = [10, 4]
        ballSpeed : list[int, int] = [1,1]

        while True:
            player = getInput()
            grid, playerPositions = updatePlatforms(grid, player, platformSize, playerPositions)
            grid, ballPosition, ballSpeed, WinState = updateBall(grid, ballPosition, ballSpeed)
            renderGrid(grid)
            time.sleep(1.0/fps)
            if WinState == Winstate.PLAYING:
                clear_console()
                continue

            if WinState == Winstate.AWON:
                print("Player A WON Ending game....")
            elif WinState == Winstate.BWON:
                print("Player B WON Ending game....")

            time.sleep(5)
            break
           
if __name__ == '__main__':
    runGame(15)
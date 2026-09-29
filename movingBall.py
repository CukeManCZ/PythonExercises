import time

def clear_console():
    print("\033[2J\033[H", end="")

def createGameGrid(width : int, height : int) -> list[list[bool]]:
    grid : list[list[bool]] = []

    for x in range(width):
        row : list[bool] = []
        for y in range(height):
            row.append(False)
        grid.append(row)

    return grid

def renderGrid(grid: list[list[bool]]) -> str: 
    finalOutput : str = "\n\n\n\n"

    # Adds - line
    finalOutput = getTopLine(grid)
    

    for x in grid:
        output : str = "|"
        for gridValue in x:
            if gridValue:
                output += " o "
            else:
                output += "   "

        output += "|\n"
        finalOutput += output

    finalOutput += "-"
    for y in grid[0]:
        finalOutput += "---"
    finalOutput += "-"

    print(finalOutput)

def getTopLine(grid: list[list[bool]]) -> str:
    finalOutput = "-"
    for y in grid[0]:
        finalOutput += "---"
    finalOutput += "-"
    finalOutput += "\n"
    return finalOutput

"""
Assuming speed is max in range (-1,1)
"""
def updateBall(grid: list[list[bool]], previousPosition : list[int, int], speed : list[int, int]) -> tuple[list[list[bool]], list[int, int], list[int, int]]:
    grid[previousPosition[0]][previousPosition[1]] = False
    width = len(grid)
    height = len(grid[0])
    
    xPosition = previousPosition[0] + speed[0]
    yPosition = previousPosition[1] + speed[1]

    #Update speed
    if(xPosition >= width):
        speed[0] = speed[0] * (-1)
    if(xPosition <= 0):
        speed[0] = speed[0] * (-1)
    if(yPosition >= height):
        speed[1] = speed[1] * (-1)
    if(yPosition <= 0):
        speed[1] = speed[1] * (-1)

    #Make sure position is in boundaries
    xPosition = min(xPosition, width-1)
    xPosition = max(xPosition, 0)
    yPosition = min(yPosition, height-1)
    yPosition = max(yPosition, 0)

    grid[xPosition][yPosition] = True

    return (grid, (xPosition, yPosition), speed)

def runGame(fps : float):
    width : int = 10
    height : int = 5
    grid : list[list[bool]] = createGameGrid(width, height)
    ballPosition : list[int, int] = [0, 0]
    ballSpeed : list[int, int] = [1,1]

    while True:
        grid, ballPosition, ballSpeed = updateBall(grid, ballPosition, ballSpeed)
        renderGrid(grid)

        time.sleep(1.0/fps)
        clear_console()   

if __name__ == '__main__':
    runGame(10)


import copy
import os
import time

def sub3x3(a, row, col):
    height = len(a)
    width = len(a[0])

    result = []
    for r in (row - 1, row, row + 1):
        new_row = []
        for c in (col - 1, col, col + 1):
            new_row.append(a[r % height][c % width])
        result.append(new_row)

    return result


def countCells(world, row, col):
    subMatrix = sub3x3(world, row, col)

    cells = 0
    for i in subMatrix:
        for j in i:
            if j == 1:
                cells += 1

    # the middle of the 3x3 is the cell itself, don't count it
    cells -= subMatrix[1][1]

    return cells


def clearConsole():
    # Windows uses "cls", Linux and macOS use "clear"
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def printWorld(world):
    for row in world:
        line = ""
        for cell in row:
            if cell == 1:
                line += "#"
            else:
                line += "."
        print(line)
    print()


#Any live cell with fewer than two live neighbours dies, as if by underpopulation.
#Any live cell with two or three live neighbours lives on to the next generation.
#Any live cell with more than three live neighbours dies, as if by overpopulation.
#Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction

def simulateLife(world, steps, waitTime):
    currentWorld = copy.deepcopy(world)

    height = len(currentWorld)
    width = len(currentWorld[0])

    # show the starting world first
    clearConsole()
    print("Step 0")
    printWorld(currentWorld)
    time.sleep(waitTime)

    for step in range(steps):
        newWorld = copy.deepcopy(currentWorld)

        for row in range(height):
            for col in range(width):
                neighbours = countCells(currentWorld, row, col)
                cell = currentWorld[row][col]

                # rule 0: live cell with fewer than 2 neighbours dies (underpopulation)
                if cell == 1 and neighbours < 2:
                    newWorld[row][col] = 0

                # rule 1: live cell with 2 or 3 neighbours lives on
                if cell == 1 and (neighbours == 2 or neighbours == 3):
                    newWorld[row][col] = 1

                # rule 2: live cell with more than 3 neighbours dies (overpopulation)
                if cell == 1 and neighbours > 3:
                    newWorld[row][col] = 0

                # rule 3: dead cell with exactly 3 neighbours becomes alive (reproduction)
                if cell == 0 and neighbours == 3:
                    newWorld[row][col] = 1

        # the whole step is finished, the new world becomes the current one
        currentWorld = copy.deepcopy(newWorld)

        clearConsole()
        print("Step", step + 1)
        printWorld(currentWorld)
        time.sleep(waitTime)

    return currentWorld


a = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
     [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
     [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

simulateLife(a, 40, 0.3)
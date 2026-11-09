import sys
import copy
from collections import deque

# 0 = free cell, 1 = wall, 2 = filled cell
GRID = [
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 1, 0, 0, 0, 1],
    [0, 0, 1, 0, 0, 0, 1, 0, 1, 0],
    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 1, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
]

# Neighbour offsets as (row_change, column_change)
DIRECTIONS_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]                      # up, down, left, right
DIRECTIONS_8 = DIRECTIONS_4 + [(-1, -1), (1, 1), (1, -1), (-1, 1)]     # + diagonals


# ---------- 1) Message decoding (stack) ----------
def decode_message(message):
    stack = []
    output = []
    for character in message:
        if character == " ":
            continue                          # spaces are ignored
        if character == "*":
            output.append(stack.pop())        # asterisk = pop to output
        else:
            stack.append(character)           # letter = push
    return "".join(output)


# ---------- 2) + 3) Flood fill: stack / queue ----------
def flood_fill(grid, start_row, start_column, mode="stack", diagonal=False, animate=False):
    """Fills the connected area of EMPTY cells starting at (start_row, start_column).

    mode = "stack" -> LIFO (takes the most recently added cell)
    mode = "queue" -> FIFO (takes the oldest added cell)

    Returns (filled_grid, max_container_size, total_pushes).
    """
    grid = copy.deepcopy(grid)                # do not modify the original
    row_count = len(grid)
    column_count = len(grid[0])
    directions = DIRECTIONS_8 if diagonal else DIRECTIONS_4

    # deque supports fast removal from both ends
    cells_to_visit = deque([(start_row, start_column)])
    max_container_size = 1
    total_pushes = 1
    step_number = 0

    while cells_to_visit:
        if mode == "stack":
            row, column = cells_to_visit.pop()        # from the end (last added)
        else:
            row, column = cells_to_visit.popleft()    # from the start (first added)

        if grid[row][column] == 0:
            grid[row][column] = 2

            for row_change, column_change in directions:
                neighbour_row = row + row_change
                neighbour_column = column + column_change
                inside_grid = (0 <= neighbour_row < row_count
                               and 0 <= neighbour_column < column_count)
                if inside_grid:
                    cells_to_visit.append((neighbour_row, neighbour_column))
                    total_pushes += 1

            step_number += 1
            if animate:
                print(f"--- step {step_number} ({mode}), cells waiting: {len(cells_to_visit)}")
                print_grid(grid)

        max_container_size = max(max_container_size, len(cells_to_visit))

    return grid, max_container_size, total_pushes


def flood_fill_efficient(grid, start_row, start_column, mode="stack"):
    """Improvement: a cell is marked as FILLED at the moment it is added,
    so no cell is ever added to the container more than once."""
    grid = copy.deepcopy(grid)
    row_count = len(grid)
    column_count = len(grid[0])

    cells_to_visit = deque()
    total_pushes = 0
    if grid[start_row][start_column] == 0:
        grid[start_row][start_column] = 2    # mark immediately
        cells_to_visit.append((start_row, start_column))
        total_pushes = 1
    max_container_size = len(cells_to_visit)

    while cells_to_visit:
        if mode == "stack":
            row, column = cells_to_visit.pop()
        else:
            row, column = cells_to_visit.popleft()

        for row_change, column_change in DIRECTIONS_4:
            neighbour_row = row + row_change
            neighbour_column = column + column_change
            inside_grid = (0 <= neighbour_row < row_count
                           and 0 <= neighbour_column < column_count)
            if inside_grid and grid[neighbour_row][neighbour_column] == 0:
                grid[neighbour_row][neighbour_column] = 2    # mark immediately
                cells_to_visit.append((neighbour_row, neighbour_column))
                total_pushes += 1

        max_container_size = max(max_container_size, len(cells_to_visit))

    return grid, max_container_size, total_pushes


def print_grid(grid):
    for row in grid:
        print(" ".join(str(cell) for cell in row))


def print_animation_preview(grid, start_row, start_column, steps_to_show=6):
    """Shows the first few fill steps for both stack and queue."""
    import io
    import contextlib
    for mode in ("stack", "queue"):
        captured_output = io.StringIO()
        with contextlib.redirect_stdout(captured_output):
            flood_fill(grid, start_row, start_column, mode, animate=True)
        step_blocks = captured_output.getvalue().split("--- step ")[1:steps_to_show + 1]
        print(f"##### {mode} #####")
        for block in step_blocks:
            print("--- step " + block, end="")


if __name__ == "__main__":
    print("Decoded message:", decode_message("TE*A*QYS***SEU****NI*O**"))
    print()

    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        start_row, start_column = map(int, input("Start point row,column: ").split(","))
        filled_grid, _, _ = flood_fill(GRID, start_row, start_column, "stack")
        print_grid(filled_grid)
        sys.exit()

    for start_row, start_column in [(4, 4), (9, 9)]:
        print(f"===== Start {start_row},{start_column} =====")

        stack_grid, stack_max_size, stack_pushes = flood_fill(GRID, start_row, start_column, "stack")
        print_grid(stack_grid)
        print(f"stack: max size={stack_max_size}, pushes={stack_pushes}")

        queue_grid, queue_max_size, queue_pushes = flood_fill(GRID, start_row, start_column, "queue")
        print(f"queue: max size={queue_max_size}, pushes={queue_pushes}, "
              f"same result={stack_grid == queue_grid}")

        diagonal_grid, _, diagonal_pushes = flood_fill(GRID, start_row, start_column, "stack", diagonal=True)
        print(f"diagonals (stack): same result={stack_grid == diagonal_grid}, pushes={diagonal_pushes}")

        efficient_stack_grid, efficient_stack_max, efficient_pushes = flood_fill_efficient(
            GRID, start_row, start_column, "stack")
        _, efficient_queue_max, _ = flood_fill_efficient(GRID, start_row, start_column, "queue")
        print(f"efficient: stack max={efficient_stack_max}, queue max={efficient_queue_max}, "
              f"pushes={efficient_pushes}, same result={stack_grid == efficient_stack_grid}")
        print()

    print("===== Animation from 4,4: first 6 steps =====")
    print_animation_preview(GRID, 4, 4)

    # Memory comparison on a larger empty grid
    SIZE = 400
    big_grid = [[0] * SIZE for _ in range(SIZE)]
    for mode in ("stack", "queue"):
        _, max_size, pushes = flood_fill(big_grid, SIZE // 2, SIZE // 2, mode)
        _, efficient_max, efficient_pushes = flood_fill_efficient(big_grid, SIZE // 2, SIZE // 2, mode)
        print(f"{SIZE}x{SIZE} empty grid, start in the middle, {mode}: "
              f"max={max_size}, pushes={pushes} | efficient: max={efficient_max}, pushes={efficient_pushes}")
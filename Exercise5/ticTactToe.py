

inputList = [["", "", "", ""],
             ["X", "", "", ""],
             ["", "", "", ""]]


def printBoard(matrix):
    for row in matrix:
        print(*row)


def winner(board):
    rows = len(board)
    cols = len(board[0])

    for r in range(rows):
        for c in range(cols):
            p = board[r][c]
            if p == "":
                continue

            # right
            if c + 2 < cols:
                if board[r][c + 1] == p and board[r][c + 2] == p:
                    return p

            # down
            if r + 2 < rows:
                if board[r + 1][c] == p and board[r + 2][c] == p:
                    return p

            # diagonal down-right
            if r + 2 < rows and c + 2 < cols:
                if board[r + 1][c + 1] == p and board[r + 2][c + 2] == p:
                    return p

            # diagonal down-left
            if r + 2 < rows and c - 2 >= 0:
                if board[r + 1][c - 1] == p and board[r + 2][c - 2] == p:
                    return p


printBoard(inputList)
print(f"Winner is: {winner(inputList)}")
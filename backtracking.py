def solve(board):
    # If board is complete, returns
    if not find_empty(board):
        return True
    else:
        row, col = find_empty(board)
    # Brute-force numbers
    for i in range(1, 10):
        if is_valid(board, i, (row, col)):
            board[row][col] = i
            if solve(board):  # Goes for next number...
                return True
            # ...and if it's incorrect backtracks
            board[row][col] = 0
    return False


def is_valid(board, num, pos):
    for i in range(9):
        if num != 0 and num == board[pos[0]][i] and pos[1] != i:  # Checks for num in a column
            return False
        elif num != 0 and num == board[i][pos[1]] and pos[0] != i:  # Checks for num in a row
            return False

    # Checks for num in a box
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if num != 0 and board[i][j] == num and (i, j) != pos:
                return False
    # Else
    return True


def find_empty(board):
    for i in range(len(board)):
        for j in range(9):
            if board[i][j] == 0:
                return i, j  # row and column
    return None

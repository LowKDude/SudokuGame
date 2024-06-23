import random

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True

def solve_sudoku(board):
    empty = find_empty_location(board)
    if not empty:
        return True
    row, col = empty
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0
    return False

def find_empty_location(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def generate_sudoku():
    board = [[0] * 9 for _ in range(9)]
    fill_diagonal_boxes(board)
    solve_sudoku(board)
    return board

def fill_diagonal_boxes(board):
    for i in range(0, 9, 3):
        fill_box(board, i, i)

def fill_box(board, row, col):
    num_list = list(range(1, 10))
    random.shuffle(num_list)
    for i in range(3):
        for j in range(3):
            board[row + i][col + j] = num_list.pop()

def remove_numbers(board, difficulty):
    removal_count = {"easy": 30, "medium": 40, "hard": 50}
    count = removal_count.get(difficulty, 30)
    while count > 0:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if board[row][col] != 0:
            board[row][col] = 0
            count -= 1
    return board

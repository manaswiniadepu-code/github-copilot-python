import copy
import random

SIZE = 9
EMPTY = 0
DIFFICULTIES = {
    'easy': 45,
    'medium': 35,
    'hard': 25,
}

def deep_copy(board):
    """Return an independent copy of a Sudoku board."""
    return copy.deepcopy(board)

def create_empty_board():
    """Create a blank Sudoku board."""
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]

def is_safe(board, row, col, num):
    """Return whether a number can be placed at a board position."""
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def fill_board(board):
    """Fill a board with a valid randomized Sudoku solution."""
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True

def count_solutions(board, limit=2):
    """Count solutions up to ``limit`` so uniqueness can be checked cheaply."""
    working_board = deep_copy(board)

    def solve():
        """Find solutions recursively, stopping after the requested limit."""
        if solve.count >= limit:
            return

        best_cell = None
        best_candidates = None
        for row in range(SIZE):
            for col in range(SIZE):
                if working_board[row][col] != EMPTY:
                    continue
                candidates = [
                    number for number in range(1, SIZE + 1)
                    if is_safe(working_board, row, col, number)
                ]
                if not candidates:
                    return
                if best_candidates is None or len(candidates) < len(best_candidates):
                    best_cell = (row, col)
                    best_candidates = candidates

        if best_cell is None:
            solve.count += 1
            return

        row, col = best_cell
        for number in best_candidates:
            working_board[row][col] = number
            solve()
            working_board[row][col] = EMPTY
            if solve.count >= limit:
                return

    solve.count = 0
    solve()
    return solve.count

def remove_cells(board, clues):
    """Remove cells while preserving a single solution and clue count."""
    if not 0 < clues <= SIZE * SIZE:
        raise ValueError('clues must be between 1 and 81')

    cells = [(row, col) for row in range(SIZE) for col in range(SIZE)]
    random.shuffle(cells)
    remaining = sum(cell != EMPTY for row in board for cell in row)

    for row, col in cells:
        if remaining <= clues:
            break
        value = board[row][col]
        if value == EMPTY:
            continue
        board[row][col] = EMPTY
        if count_solutions(board) == 1:
            remaining -= 1
        else:
            board[row][col] = value

    if remaining != clues:
        raise ValueError('Could not remove cells while preserving uniqueness')

def generate_puzzle(clues=35):
    """Generate a puzzle with the requested clues and one unique solution."""
    if not 0 < clues <= SIZE * SIZE:
        raise ValueError('clues must be between 1 and 81')

    board = create_empty_board()
    fill_board(board)
    solution = deep_copy(board)
    try:
        remove_cells(board, clues)
    except ValueError:
        return generate_puzzle(clues)
    puzzle = deep_copy(board)
    return puzzle, solution

def generate_puzzle_for_difficulty(difficulty):
    """Generate a puzzle for a named difficulty level."""
    try:
        clues = DIFFICULTIES[difficulty.lower()]
    except (AttributeError, KeyError) as error:
        raise ValueError('difficulty must be easy, medium, or hard') from error
    return generate_puzzle(clues)

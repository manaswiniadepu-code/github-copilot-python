from sudoku_logic import (
    EMPTY,
    SIZE,
    create_empty_board,
    count_solutions,
    deep_copy,
    fill_board,
    generate_puzzle_for_difficulty,
    generate_puzzle,
    is_safe,
    remove_cells,
)


def test_create_empty_board_has_expected_shape_and_values():
    board = create_empty_board()

    assert len(board) == SIZE
    assert all(len(row) == SIZE for row in board)
    assert all(cell == EMPTY for row in board for cell in row)


def test_deep_copy_is_independent():
    board = create_empty_board()
    copied_board = deep_copy(board)
    copied_board[0][0] = 1

    assert board[0][0] == EMPTY
    assert copied_board[0][0] == 1


def test_is_safe_rejects_row_column_and_box_conflicts():
    board = create_empty_board()
    board[0][0] = 1
    board[1][4] = 2
    board[1][1] = 3

    assert is_safe(board, 0, 1, 1) is False
    assert is_safe(board, 2, 4, 2) is False
    assert is_safe(board, 2, 2, 3) is False
    assert is_safe(board, 8, 8, 4) is True


def test_fill_board_creates_a_valid_solution():
    board = create_empty_board()

    assert fill_board(board) is True
    assert all(set(row) == set(range(1, SIZE + 1)) for row in board)
    assert all(
        {board[row][column] for row in range(SIZE)} == set(range(1, SIZE + 1))
        for column in range(SIZE)
    )


def test_remove_cells_preserves_requested_number_of_clues():
    board = create_empty_board()
    fill_board(board)

    remove_cells(board, clues=40)

    assert sum(cell != EMPTY for row in board for cell in row) == 40


def test_generate_puzzle_returns_matching_puzzle_and_solution():
    puzzle, solution = generate_puzzle(clues=35)

    assert all(len(row) == SIZE for row in puzzle)
    assert all(len(row) == SIZE for row in solution)
    assert all(set(row) == set(range(1, SIZE + 1)) for row in solution)
    assert all(
        {solution[row][column] for row in range(SIZE)} == set(range(1, SIZE + 1))
        for column in range(SIZE)
    )
    assert all(
        puzzle[row][column] in (EMPTY, solution[row][column])
        for row in range(SIZE)
        for column in range(SIZE)
    )
    assert sum(cell != EMPTY for row in puzzle for cell in row) == 35
    assert count_solutions(puzzle) == 1


def test_difficulties_have_expected_clue_counts_and_unique_solutions():
    expected_clues = {'easy': 45, 'medium': 35, 'hard': 25}

    for difficulty, clues in expected_clues.items():
        puzzle, solution = generate_puzzle_for_difficulty(difficulty)

        assert sum(cell != EMPTY for row in puzzle for cell in row) == clues
        assert count_solutions(puzzle) == 1
        assert all(
            puzzle[row][column] in (EMPTY, solution[row][column])
            for row in range(SIZE)
            for column in range(SIZE)
        )
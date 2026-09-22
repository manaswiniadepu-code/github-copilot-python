from flask import Flask, render_template, jsonify, request
import sudoku_logic

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None
}

@app.route('/')
def index():
    """Render the Sudoku game."""
    return render_template('index.html')

@app.route('/new')
def new_game():
    """Create and store a new puzzle at the requested difficulty."""
    difficulty = request.args.get('difficulty', 'medium')
    try:
        puzzle, solution = sudoku_logic.generate_puzzle_for_difficulty(difficulty)
    except ValueError as error:
        return jsonify({'error': str(error)}), 400
    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    return jsonify({'difficulty': difficulty.lower(), 'puzzle': puzzle})

@app.route('/check', methods=['POST'])
def check_solution():
    """Validate Sudoku conflicts and compare entries with the solution."""
    board = _get_submitted_board()
    if board is None:
        return jsonify({'error': 'A valid board is required'}), 400
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    incorrect = []
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if board[i][j] != solution[i][j]:
                incorrect.append([i, j])
    conflicts = [list(cell) for cell in sudoku_logic.find_conflicts(board)]
    return jsonify({'incorrect': incorrect, 'conflicts': conflicts})

@app.route('/hint', methods=['POST'])
def get_hint():
    """Return one solution value for an empty cell in the submitted board."""
    board = _get_submitted_board()
    if board is None:
        return jsonify({'error': 'A valid board is required'}), 400
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    for row in range(sudoku_logic.SIZE):
        for col in range(sudoku_logic.SIZE):
            if board[row][col] == sudoku_logic.EMPTY:
                return jsonify({'row': row, 'col': col, 'value': solution[row][col]})
    return jsonify({'error': 'There are no empty cells'}), 400

def _get_submitted_board():
    """Return a valid board from the request, or ``None``."""
    data = request.json
    if not isinstance(data, dict) or not isinstance(data.get('board'), list):
        return None
    board = data['board']
    if len(board) != sudoku_logic.SIZE or any(
        not isinstance(row, list) or len(row) != sudoku_logic.SIZE
        or any(not isinstance(cell, int) or cell < 0 or cell > sudoku_logic.SIZE for cell in row)
        for row in board
    ):
        return None
    return board

if __name__ == '__main__':
    app.run(debug=True)
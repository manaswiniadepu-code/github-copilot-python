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
    """Compare the submitted board with the current game's solution."""
    data = request.json
    if not isinstance(data, dict) or not isinstance(data.get('board'), list):
        return jsonify({'error': 'A valid board is required'}), 400
    board = data.get('board')
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    if len(board) != sudoku_logic.SIZE or any(
        not isinstance(row, list) or len(row) != sudoku_logic.SIZE for row in board
    ):
        return jsonify({'error': 'A valid board is required'}), 400
    incorrect = []
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if board[i][j] != solution[i][j]:
                incorrect.append([i, j])
    return jsonify({'incorrect': incorrect})

if __name__ == '__main__':
    app.run(debug=True)
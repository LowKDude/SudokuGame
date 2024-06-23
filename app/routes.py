from flask import request, jsonify, render_template
from app import app, db
from app.models import SudokuGame
from app.sudoku_generator import generate_sudoku, remove_numbers
from sqlalchemy import desc


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def start_game():
    data = request.json
    username = data.get('username')
    difficulty = data.get('difficulty')
    # Generate a Sudoku grid based on difficulty
    complete_grid = generate_sudoku()
    puzzle_grid = remove_numbers(complete_grid, difficulty)
    new_game = SudokuGame(username=username, difficulty=difficulty)
    db.session.add(new_game)
    db.session.commit()
    return jsonify({'grid': puzzle_grid, 'game_id': new_game.id})


@app.route('/validate_move', methods=['POST'])
def validate_move():
    data = request.json
    grid = data.get('grid')
    row = data.get('row')
    col = data.get('col')
    num = data.get('num')

    if not is_valid_move(grid, row, col, num):
        return jsonify({'valid': False})

    return jsonify({'valid': True})


@app.route('/previous_games', methods=['GET'])
def previous_games():
    games = SudokuGame.query.order_by(desc(SudokuGame.start_time)).limit(10).all()
    game_list = [
        {
            'id': game.id,
            'username': game.username,
            'difficulty': game.difficulty,
            'start_time': game.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': game.end_time.strftime('%Y-%m-%d %H:%M:%S') if game.end_time else None
        }
        for game in games
    ]
    return jsonify(game_list)


def is_valid_move(grid, row, col, num):
    # Check row
    for j in range(9):
        if j != col and grid[row][j] == num:
            return False

    # Check column
    for i in range(9):
        if i != row and grid[i][col] == num:
            return False

    # Check 3x3 subgrid
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if (i != row or j != col) and grid[i][j] == num:
                return False

    return True


def validate_sudoku_solution(grid, solution):
    def is_valid_group(group):
        group = [num for num in group if num != 0]
        return len(group) == len(set(group)) and all(1 <= num <= 9 for num in group)

    # Ensure that the original grid's filled cells match the solution
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0 and grid[i][j] != solution[i][j]:
                return False

    return (
            all(is_valid_group(row) for row in solution) and
            all(is_valid_group(col) for col in zip(*solution)) and
            all(
                is_valid_group([
                    solution[x][y]
                    for x in range(i, i + 3)
                    for y in range(j, j + 3)
                ])
                for i in range(0, 9, 3)
                for j in range(0, 9, 3)
            )
    )

from flask import Flask, render_template, request, jsonify
from checkmate_solver import solve_checkmate, save_board_svg
import chess
import chess.svg
app = Flask(__name__)

previous_k = 1
current_board = 0
fens = []

def read_file_lines(file_path):
    lines = []
    with open(file_path, 'r') as file:
        for line in file:
            lines.append(line.strip())
    return lines

@app.route("/")
def index():
    return render_template(
        "index.html",
    )

@app.route('/generate-board', methods=['POST'])
def generate_board():
    global previous_k
    global current_board
    global fens
    data = request.json
    if previous_k == int(data['moves']) and len(fens)>0:
        current_board += 1
        if current_board >= len(fens):
            current_board = 0
    else:
        file_path = "static/mate-in-" + data['moves'] + ".txt"
        fens = read_file_lines(file_path)
        current_board = 0
        previous_k = int(data['moves'])
    board = chess.Board(fens[current_board])
    save_board_svg(board, 0)
    return jsonify(image_index=0, board_number=current_board)

@app.route('/solve-board', methods=['GET'])
def solve_board():
    board = chess.Board(fens[current_board])
    result_moves, time = solve_checkmate(fens[current_board], previous_k)
    text = ""
    if board.turn:
        text = "First move: white player"
    else:
        text = "First move: black player"
    return jsonify(number_of_images = previous_k*2, text=text, moves=result_moves, time=time)


if __name__ == '__main__':
    app.run(debug=True)
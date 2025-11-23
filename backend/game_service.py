from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def check_winner(board):
    lines = board + [list(col) for col in zip(*board)]
    lines.append([board[i][i] for i in range(3)])
    lines.append([board[i][2-i] for i in range(3)])
    for line in lines:
        if line[0] and line.count(line[0]) == 3:
            return line[0]
    if all(cell for row in board for cell in row):
        return "Draw"
    return None

def new_board():
    return [[None, None, None],[None, None, None],[None, None, None]]

@app.get("/api/reset")
def reset():
    return jsonify({"board": new_board(), "turn": "X", "winner": None})

@app.post("/api/move")
def move():
    data = request.get_json(force=True)
    board = data.get("board")
    turn = data.get("turn", "X")
    row, col = data["row"], data["col"]

    if board[row][col] is None:
        board[row][col] = turn
    winner = check_winner(board)
    next_turn = None if winner else ("O" if turn == "X" else "X")
    return jsonify({"board": board, "turn": next_turn, "winner": winner})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

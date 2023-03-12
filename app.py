from flask import Flask, request

import os
import objects as battle_objects
import logic as battle_logic

app = Flask(__name__)

# Game state
game = None
turn = 0
board = None
you = None

# GET / endpoint
@app.route('/', methods=['GET'])
def get_game_info():
    return {
        "apiversion": "1",
        "version": "0.1.0",
        "author": "ianeen",
        "color": "#420420",
        "head": "silly",
        "tail": "pixel"
    }

# POST /start endpoint
@app.route('/start', methods=['POST'])
def start_game():
    global game, turn, board, you

    # Set initial game state
    d_game = request.json.get('game', game)
    turn = request.json.get('turn', turn)
    d_board = request.json.get('board', board)
    d_you = request.json.get('you', you)

    # Create objects for the game, board, and you
    game = battle_objects.Game(d_game["id"], d_game["ruleset"], d_game["map"], d_game["timeout"], d_game["source"])
    board = battle_objects.Board(d_board["height"], d_board["width"], d_board["food"], d_board["hazards"], d_board["snakes"])
    you = battle_objects.Snake(d_you["id"], d_you["name"], d_you["health"], d_you["body"], d_you["latency"], d_you["head"], d_you["length"], d_you["shout"], d_you["squad"], d_you["customizations"])

    response = "Game started!"
    print(response)
    return response

# POST /move endpoint
@app.route('/move', methods=['POST'])
def make_move():
    global game, turn, board, you

    # Get new updated game state
    d_game = request.json.get('game', game)
    turn = request.json.get('turn', turn)
    d_board = request.json.get('board', board)
    d_you = request.json.get('you', you)

    # Update objects for the game and board
    board = battle_objects.Board(d_board["height"], d_board["width"], d_board["food"], d_board["hazards"], d_board["snakes"])
    you = battle_objects.Snake(d_you["id"], d_you["name"], d_you["health"], d_you["body"], d_you["latency"], d_you["head"], d_you["length"], d_you["shout"], d_you["squad"], d_you["customizations"])
    print(board)

    # Move logic
    move = battle_logic.make_move(board, you)
    shout = f"Moving {move} in the world..."

    print(shout)

    # Send move response
    return {
        "move": move,
        "shout": shout
    }

# POST /end endpoint
@app.route('/end', methods=['POST'])
def end_game():
    global game, turn, board, you

    d_game = request.json.get('game', game)
    d_turn = request.json.get('turn', turn)
    d_board = request.json.get('board', board)
    d_you = request.json.get('you', you)

    response = "Game ended!"
    print(response)
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 33507))
    app.run(host='0.0.0.0', port=port)

# --------- Global Variables -----------
board = ["-"] * 9
game_still_going = True
winner = None
current_player = "X"

# Reset the game
def reset_game():
    global board, game_still_going, winner, current_player
    board = ["-"] * 9
    game_still_going = True
    winner = None
    current_player = "X"

# Handle a move from frontend
def make_move(position):
    global board, current_player, game_still_going, winner

    if not game_still_going or board[position] != "-":
        return {"board": board, "winner": winner, "player": current_player, "error": "Invalid move"}

    board[position] = current_player
    check_if_game_over()

    if not game_still_going:
        return {"board": board, "winner": winner, "player": current_player}

    flip_player()
    return {"board": board, "winner": winner, "player": current_player}


# ----- Game Logic -----
def check_if_game_over():
    check_for_winner()
    check_for_tie()

def check_for_winner():
    global winner, game_still_going
    win_patterns = [
        [0,1,2],[3,4,5],[6,7,8],  # rows
        [0,3,6],[1,4,7],[2,5,8],  # cols
        [0,4,8],[2,4,6]           # diags
    ]
    for pattern in win_patterns:
        if board[pattern[0]] == board[pattern[1]] == board[pattern[2]] != "-":
            winner = board[pattern[0]]
            game_still_going = False
            return

def check_for_tie():
    global game_still_going
    if "-" not in board and winner is None:
        game_still_going = False

def flip_player():
    global current_player
    current_player = "O" if current_player == "X" else "X"

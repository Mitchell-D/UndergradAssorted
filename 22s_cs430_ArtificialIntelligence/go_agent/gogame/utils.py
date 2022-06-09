import time
import os
from colorama import Fore
import pickle as pkl

from gogame.goboard import GameState
from gogame.gotypes import Player, Point
from gogame.agent.naive import RandomBot

# Maps each player to their stone character
stone_to_char = {
        None:'.',
        Player.black:Fore.BLUE+'x'+Fore.WHITE,
        Player.white:Fore.RED+'o'+Fore.WHITE,
        }

# Print the current board state. Assumes board is square
def print_board(board, clear_on_move=True):
    cols = [chr(ord('@')+n) for n in range(1,board.get_row_count()+1)]
    if clear_on_move: print(chr(27)+"[2J")
    print(4*' '+'*'+(board.get_col_count()+1)*'--'+"*")
    for i in range(board.get_row_count(), 0, -1):
        line = []
        for j in range(1, board.get_col_count()+1):
            stone = board.get_stone(Point(i,j))
            line.append(stone_to_char[stone]+" ")
        print(f"{i:3} | {''.join(line)}|")
    print(4*' '+'*'+(board.get_col_count()+1)*'--'+"*")
    print(6*' '+' '.join(cols))

# Print this player and their move.
def print_move(player, move, turn):
    """ print a string describing the next move  """
    if move.is_pass: move_str = "passes this turn"
    elif move.is_resign: move_str = "resigns"
    else: move_str = f"({move.point.col_letter()}, {move.point.row})"
    print(f"Turn {turn} {player} ({stone_to_char[player]}) places at {move_str}")

def update_times(turn_times, timefile):
    with open(timefile, "rb") as timefp:
        times = pkl.load(timefp)
    times.append(turn_times)
    with open(timefile, "wb") as timefp:
        pkl.dump(times, timefp)

# Initialize the game with bot a and bot b
def start_bots_game(board_size, update_freq, bot_a, bot_b,
        sequence=None, capture_turntime=False):
    bots = { Player.white:bot_a, Player.black:bot_b }
    game = GameState.new_game(board_size)
    c = 1
    times = [0]
    last_time = time.time()
    while not game.is_over():
        # Determine which player's turn it is.
        print(f"\n\nBoard state before move {c} by {game.next_player}:")
        print_board(game.board, False)

        # Get this player's next move and play it
        if sequence == None:
            move = bots[game.next_player].get_move(game)
        elif sequence != None and len(sequence):
            move = sequence.pop(0)
        else:
            break
        print_move(game.next_player, move, c)
        game = game.apply_move(move)
        new_time = time.time()
        times.append(new_time-last_time)
        last_time = new_time
        time.sleep(update_freq)
        c+=1
    return times

def point_from_coords(coords):
    return Point(int(coords[1:]), ord(coords[0].lower())-96)

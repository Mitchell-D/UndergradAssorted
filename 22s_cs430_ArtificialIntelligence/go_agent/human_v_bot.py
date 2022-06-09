from gogame.agent.naive import RandomBot
from gogame.goboard import GameState, Move
from gogame.gotypes import Player
from gogame.utils import print_board, print_move, point_from_coords

def start_game():
    board_size = 9
    game = GameState.new_game(board_size)
    bot = RandomBot(board_size)
    c=1
    while not game.is_over():
        print(chr(27)+"[2J")
        print_board(game.board, False)
        if game.next_player == Player.black:
            human_move = input("-- ")
            point = point_from_coords(human_move.strip())
            move = Move.play(point)
        else:
            move = bot.get_move(game)
        print_move(game.next_player, move, c)
        game = game.apply_move(move)
        c+=1

if __name__=="__main__":
    start_game()

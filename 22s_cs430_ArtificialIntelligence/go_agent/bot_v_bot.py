from gogame.goboard import GameState, Move
from gogame.gotypes import Player, Point
from gogame.agent.naive import RandomBot
from gogame.utils import start_bots_game, update_times

# Board size and update frequency. Assumes board is square.
size = 9
freq = .1
timefile = "/home/krttd/uah/22.s/cs430/hw3/turn_times.pkl"

capture_sequence = [
    Move.play(Point(row=5, col=10)),
    Move.play(Point(row=6, col=10)),
    Move.play(Point(row=5, col=11)),
    Move.play(Point(row=6, col=11)),
    Move.play(Point(row=6, col=9)),
    Move.play(Point(row=1, col=1)),
    Move.play(Point(row=6, col=12)),
    Move.play(Point(row=2, col=1)),
    Move.play(Point(row=7, col=10)),
    Move.play(Point(row=3, col=1)),
    Move.play(Point(row=7, col=11)),
    Move.play(Point(row=4, col=1))]

if __name__=="__main__":
    for i in range(5):
        times = start_bots_game(
            board_size=size,
            update_freq=freq,
            bot_a=RandomBot(size),
            bot_b=RandomBot(size),
            #sequence=capture_sequence
            )
        update_times(times, timefile)

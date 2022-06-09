import random

from gogame.gotypes import Point
from gogame.agent.base import Agent
from gogame.goboard import Move
from gogame.agent.helpers import is_point_an_eye

class RandomBot(Agent):
    def __init__(self, board_size):
        """ @param board_size: int or tuple representing (rows, cols) """
        if isinstance(board_size, int):
            board_size = (board_size, board_size)
        elif not isinstance(board_size, tuple):
            raise ValueError("Board size must either be a 2-tuple or an int.")
        self._r, self._c = board_size
        self._cur_game_state = None

    def is_valid_move(self, candidate):
        """ Determine if a move is valid given the current game state """
        is_valid = self._cur_game_state.is_valid_move(Move.play(candidate))
        is_eye = is_point_an_eye(self._cur_game_state.board, candidate,
            self._cur_game_state.next_player)
        if is_eye:
            print(f"({candidate.col_letter()}, {candidate.row}) is an eye.")
        return is_valid and not is_eye

    def get_candidates(self):
        """ Returns a list of all available valid moves """
        return list(filter( self.is_valid_move,
            [ Point(i,j) for i in range(1, self._r+1)
                for j in range(1,self._c+1) ]))

    def get_move(self, game_state):
        """ Choose a random move from a list of valid ones. """
        self._cur_game_state = game_state
        cands = self.get_candidates()
        #print("Possible moves:",cands)
        if not cands: return Move.pass_turn()
        return Move.play(random.choice(cands))

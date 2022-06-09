from gogame.gotypes import Player, Point
import copy
from gogame import zobrist

class Move():
    """ Class representing all possible game actions """
    def __init__(self, point=None, is_pass=False, is_resign=False):
        assert (point is not None) ^ is_pass ^ is_resign
        self.point = point
        self.is_play = self.point is not None
        self.is_pass = is_pass
        self.is_resign = is_resign

    @classmethod
    def play(cls, point):
        """ Return a move putting a stone at the provided point """
        return Move(point=point)

    @classmethod
    def pass_turn(cls):
        """ Return a pass move. """
        return Move(is_pass=True)

    @classmethod
    def resign(cls):
        """ Return a resignation move. """
        return Move(is_resign=True)

class Board():
    def __init__(self, row_count, col_count):
        self._nrows = row_count
        self._ncols = col_count
        self._grid = {}
        self._hash = zobrist.EMPTY_BOARD

    def get_row_count(self):
        return self._nrows

    def get_col_count(self):
        return self._ncols

    def put_stone(self, player, point, real_move):
        #  Make sure the provided point is unoccupied and on the grid
        assert self.is_on_grid(point)
        assert self._grid.get(point) is None
        adjacent_same_color = []
        adjacent_opposite_color = []
        liberties = []
        for neighbor in point.neighbors():
            #  Don't consider points off the grid.
            if not self.is_on_grid(neighbor):
                continue
            neighbor_string = self._grid.get(neighbor)
            if neighbor_string is None:
                liberties.append(neighbor)
            #  Append neighbors of the same color to the appropriate array
            elif neighbor_string.color == player:
                if neighbor_string not in adjacent_same_color:
                    adjacent_same_color.append(neighbor_string)
            #  Append neighbors of opposite color to the appropriate array
            else:
                if neighbor_string not in adjacent_opposite_color:
                    adjacent_opposite_color.append(neighbor_string)
        #  Make a new gostring for this point, assigning its liberties.
        new_string = GoString(player, [point], liberties)
        for same_color_string in adjacent_same_color:
            new_string = new_string.merged_with(same_color_string)
        #  Set all stones in this group to the new merged string
        for new_string_point in new_string.stones:
            self._grid[new_string_point] = new_string
        self._hash ^= zobrist.HASH_CODE[point, player]
        #  Remove the liberty of this point from the adjacent opposite group
        for other_color_string in adjacent_opposite_color:
            replacement = other_color_string.without_liberty(point)
            if replacement.num_liberties:
                self._replace_string(replacement)
            else:
                self._remove_string(other_color_string, real_move)
            other_color_string.remove_liberty(point)
        """
        #  Remove adjacent opponent strings with no liberties remaining.
        for other_color_string in adjacent_opposite_color:
            if other_color_string.num_liberties == 0:
                self._remove_string(other_color_string, real_move)
        """

    def _replace_string(self, new_string):
        """ Replace an entire former string with a new one. """
        for point in new_string.stones:
            self._grid[point] = new_string

    def _remove_string(self, string, real_move):
        """ Remove a string once it has been surrounded. """
        if real_move: print("removing points:",[
            (s.col_letter(), s.row) for s in string.stones])
        for point in string.stones:
            for neighbor in point.neighbors():
                neighbor_string = self._grid.get(neighbor)
                if neighbor_string is None:
                    continue
                if neighbor_string is not string:
                    self._replace_string(neighbor_string.with_liberty(point))
                    #neighbor_string.add_liberty(point)
            self._grid[point] = None
            self._hash ^= zobrist.HASH_CODE[point, string.color]

    def zobrist_hash(self):
        return self._hash

    def get_stone(self, point):
        string = self._grid.get(point)
        if string is None: return None
        return string.color

    def is_on_grid(self, point):
        return 1<=point.row<=self._nrows and 1<=point.col<=self._ncols

    def get_go_string(self, point):
        """ Return the contiguous string associated with a point """
        string = self._grid.get(point)
        if string is None: return None
        return string


class GameState():
    def __init__(self, board, next_player, previous, last_move):
        self.board = board
        self.next_player = next_player
        self.previous_state = previous
        self.last_move = last_move
        if self.previous_state is None:
            self.previous_states = frozenset()
        else:
            self.previous_states = frozenset(previous.previous_states |
                    {(previous.next_player, previous.board.zobrist_hash())})

    @classmethod
    def new_game(cls, board_size):
        if isinstance(board_size, int):
            board_size = (board_size, board_size)
        board = Board(*board_size)
        return GameState(board, Player.black, None, None)

    def apply_move(self, move):
        """ Apply a Move class to the board. """
        #  If the move places a stone, make a new board with the chosen
        #  stone placement and generate a new GameState
        if move.is_play:
            next_board = copy.deepcopy(self.board)
            next_board.put_stone(self.next_player,
                    move.point, real_move=True)
        #  If the next move doesn't involve placing a stone, the new game
        #  state is the same as the onld one.
        else:
            next_board = self.board
        #  Generate a new GameState with the updated board, marking this
        #  board as the previous one.
        return GameState(next_board, self.next_player.opponent, self, move)

    def is_over(self):
        #  The game can't be over on the first move.
        if self.last_move is None:
            return False
        #  If the opponent resigned, the game is over.
        if self.last_move.is_resign:
            return True
        #  If both players pass, the game is stalemated.
        second_last_move = self.previous_state.last_move
        if second_last_move is None:
            return False
        return self.last_move.is_pass and second_last_move.is_pass

    def is_valid_move(self, move):
        if self.is_over(): return False
        if move.is_pass or move.is_resign:
            return True
        return self.board.get_stone(move.point) is None \
                and not self.is_move_self_capture(self.next_player, move) \
                and not self.does_move_violate_ko(self.next_player, move)

    def is_move_self_capture(self, player, move):
        """ Determine if a move results in suicide, which is illegal """
        if not move.is_play: return False
        next_board = copy.deepcopy(self.board)
        next_board.put_stone(player, move.point, real_move=False)
        new_string = next_board.get_go_string(move.point)
        return not new_string.num_liberties

    @property
    def situation(self):
        """ Return a tuple wrapping the player and the board state """
        return (self.next_player, self.board)

    def does_move_violate_ko(self, player, move):
        """ Determine if a move sequence has been repeated """
        if not move.is_play: return False
        next_board = copy.deepcopy(self.board)
        next_board.put_stone(player, move.point, real_move=False)
        next_sit = (player.opponent, next_board.zobrist_hash())
        return next_sit in self.previous_states
        """
        next_sit = (player.opponent, next_board)
        past_state = self.previous_state
        while past_state is not None:
            if past_state.situation == next_sit:
                return True
            past_state = past_state.previous_state
        return False
        """

class GoString():
    def __init__(self, color, stones, liberties):
        self.color = color
        self.stones = set(stones)
        self.liberties = set(liberties)

    def remove_liberty(self, point):
        self.liberties.remove(point)

    def add_liberty(self, point):
        self.liberties.add(point)

    def merged_with(self, go_string):
        assert go_string.color == self.color
        combined_stones = self.stones | go_string.stones
        return GoString(self.color, combined_stones,
                (self.liberties | go_string.liberties) - combined_stones)

    def without_liberty(self, point):
        new_liberties = self.liberties - set([point])
        return GoString(self.color, self.stones, new_liberties)

    def with_liberty(self, point):
        new_liberties = self.liberties | set([point])
        return GoString(self.color, self.stones, new_liberties)

    @property
    def num_liberties(self):
        return len(self.liberties)

    def __eq__(self, other):
        return isinstance(other, GoString) \
            and self.color == other.color \
            and self.stones == other.stones \
            and self.liberties == other.liberties

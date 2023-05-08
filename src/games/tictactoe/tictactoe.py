#!/usr/bin/env python3

from enum import Enum
## import copy
#from interface import Interface

class CellValue(Enum):
    """Represents the state of a single cell on the board

    """
    
    EMPTY = 1
    X = 2
    O = 3
    
    def to_float(self):
        """So Scikit learn can interpret
        
        """
        if self.value == EMPTY:
            return 0.0
        elif self.value == X:
            return 1.0
        elif self.value == O:
            return 2.0
    
    def __str__(self):
        if self.value == EMPTY:
            return '_'
        elif self.value == X:
            return 'x'
        elif self.value == O:
            return 'o'
        else:
            return '?'

class Board:
    """Represents the tic tac toe board full of CellValues
    0 1 2     or as row/col    [0,0]  [0,1]   [0,2]
    3 4 5                      [1,0]  [1,1]   [1,2]
    6 7 8                      [2,0]  [2,1]   [2,2]
    """
    def __init__(self, copy_board):
        if copy_board:
            self.board = copy_board.copy()
        else:
            self.board = [
                CellValue.EMPTY, CellValue.EMPTY, CellValue.EMPTY,
                CellValue.EMPTY, CellValue.EMPTY, CellValue.EMPTY,
                CellValue.EMPTY, CellValue.EMPTY, CellValue.EMPTY
            ]

        all_sets = []
        # horizontals
        all_sets.append( [0, 1, 2] )
        all_sets.append( [3, 4, 5] )
        all_sets.append( [6, 7, 8] )
        # verticals
        all_sets.append( [0, 3, 6] )
        all_sets.append( [1, 4, 7] )
        all_sets.append( [2, 5, 8] )
        # diagonals
        all_sets.append( [0, 4, 8] )
        all_sets.append( [2, 4, 6] )
        self.all_sets_indexes_that_win = all_sets

    def get_cell(self, index):
        return self.board[index]

    def set_cell(self, row, col, cellvalue):
        # BIG TODO: type of cellvalue?  int or CellValue
        self.board[row * 3 + col] = cellvalue
        
    def get_cell_rowcol(self, row, col):
        return self.get_cell( row * 3 + col )

    def is_cell_empty(self, row, col):
        return self.get_cell_rowcol(row, col) == CellValue.EMPTY

    def get_opposite_index(self, index):
        if (index == 0):
            return 2
        if (index == 1):
            return 1
        if (index == 2):
            return 0

    def get_opposite_rowcol(self, rowcol: list[int]) -> list[int]:
        (r, c) = rowcol
        return [ self.get_opposite_index(r), self.get_opposite_index(c) ]

    def compare_moves(self, rowcol_one: list[int], rowcol_two: list[int]) -> bool:
        if not instance(rowcol_one, list):
            raise Exception("rowcol_one must be an array")
        if not instance(rowcol_two, list):
            raise Exception("rowcol_two must be an array")
        if len(rowcol_one) != len(rowcol_two):
            raise Exception(f"lengths must be the same {len(rowcol_one)} and {len(rowcol_two)}")
        for v1, v2 in zip(rowcol_one, rowcol_two):
            if (v1 != v2):
                return False
        return True
    def find_matching_move(find_row_column: list[int], list_row_columns: list[int]) -> bool:
        if not instance(find_row_column, list):
            raise Exception("find_row_column must be an array")
        if not instance(list_row_columns, list):
            raise Exception("list_row_columns must be an array")
        for i in range(len(list_row_columns)):
            target = list_row_columns[i]
            if (self.compare_moves(find_row_columns, target)):
                return True
        return False

    def check_player_throw(self, player):
        if player is None or not player:
            raise Exception("Must supply non-null 'player' argument")

    # TODO: rename -- this returns [r,c] list of cells that are EMPTY
    def list_empty():
        rtn = []
        for r in range(3):
            for c in range(3):
                if self.is_cell_empty( [r, c] ):
                    rtn.append( [r, c] )


    def compute_move_win_for(self, player):
        self.check_player_throw(player)
        wins = self.compute_list_move_wins_for(player)
        if wins:
            return wins[0]
        else:
            return None

    def compute_list_move_wins_for(self, player):
        self.check_player_throw(player)
        rtn = []
        items = self.list_empty()
        for i in range(items):
            move = items[i]
            if self.does_move_win_for(player, move):
                rtn.append(move)
        return rtn

    def does_move_win_for(player, move_row_column):
        self.check_player_throw(player)
        testboard = Board(this.board)
        testboard.set_cell(move_row_column[0], move_row_column[1], player)
        originalEmpty = self.list_empty()
        nowEmpty = self.list_empty()
        winner = testboard.winner()
        rtn = (winner == player)
        return rtn

    # A fork move is a move that creates 2 winning moves
    def compute_move_forks_for(player):
        self.check_player_throw(player)
        moves = self.list_move_forks_for(player)
        if len(moves) > 0:
            return moves[0]
        else:
            return None

    def list_move_forks_for(self, player):
        rtn = []
        items = self.list_empty()
        for i in range(len(items)):
            move_row_column = items[i]
            testboard = Board(this.board)
            testboard.set_cell(move_row_column[0], move_row_column[1], player)
            winningMoves = testboard.compute_list_move_wins_for(player)
            if len(winningMoves) >= 2:
                rtn.append(move_row_column)
        return rtn

    # Note that "player" is a different sense for this method -
    #    i.e. this returns a move that will BLOCK player, not help player
    def compute_block_fork_move(self, player, opponent):
        self.check_player_throw(player)
        rtn = None
        listForkMoves = self.list_move_forks_for_player(player)
        if len(listForkMoves) > 0:
            items = self.list_empty()
            for i in range(len(items)):
                moveRowColumn = items[i]
                testboard = Board(self.board)
                testboard.set_cell(moveRowColumn[0], moveRowColumn[1], opponent)
                opponentWinningMoves = testboard.compute_list(move_wins_for(oppponent))
                for m in range(len(opponentWinningMoves)):
                    check = opponentWinningMoves[m]
                    if self.find_maatching_move(check, listForkMoves):
                        # if opponent winning move and player's for move are the same,
                        #    then "moveRowColumn" does not work.
                        #    skip it.
                        pass
                    else:
                        if rtn is None:
                            rtn = moveRowColumn
                        break
        #else:
           # print(f"player {player} does not have a fork move")

        return rtn

    corners = [ [0,0], [0,2], [2,0], [2,2] ]

    def find_first_empty_corner(self):
        return self.find_first_empty(Board.corners)

    sides = [ [0,1], [1,0], [1,2], [2,1] ]

    def find_first_empty_side(self):
        return self.find_first_empty(sides)

    def find_first_empty(self, moves):
        rtn = None
        for i in range(len(moves)):
            move = moves[i]
            if ((rtn is None) and (self.is_cell_empty(move[0], move[1]))):
                rtn = move
        return rtn

    def find_opposite_corner_move(self, player):
        self.check_player_throw(player)
        rtn = None
        for move in Board.corners:
            if self.get_cell_rowcol(move[0], move[1]) == player:
                opposite = self.get_opposite_rowcol(move)
                if self.is_cell_empty(opposite[0], opposite[1]):
                    rtn = [ opposite[0], opposite[1] ]
        return rtn

    def count_empty(self):
        count = 0
        for r in range(3):
            for c in range(3):
                if self.is_cell_empty(r, c):
                    count = count + 1
        return count
    

    def get_winner(self):
        """ Return CellValue X/O if three in a row somewhere, or
               None if there is no winner
        """


        def _create_set_from_array( index_array: list[int] ):
            return _create_set(index_array[0], index_array[1], index_array[2])
        def _create_set(a: int, b: int, c: int):
            return set( [self.board[a], self.board[b], self.board[c]] )
        def _check_set( set_to_check ):
            """ Return True if set contains single value AND
                            that value is not CellValue.EMPTY
            """
            if CellValue.EMPTY not in set_to_check and len(set_to_check) == 1:
                return True
            return False

        winner = None
        all_sets = []
        for index_set in self.all_sets_indexes_that_win:
            all_sets.append( _create_set_from_array(index_set) )
        
        for candidate_set in all_sets:
            if _check_set( candidate_set ):
                winner = candidate_set[0]
        return winner

    def strategy_log(msg: str):
        if (False):
            print(msg)

    #// STRATEGY: "perfect"
    #//  pick cell that wins, else cell that blocks,
    #//  else cell that forks, else cell that blocks fork,
    #//  else middle, else opposite corner,
    #//  else random corner, else random side
    def strategy_perfect(computerPlayer, humanPlayer):
        winComputer = self.compute_move_win_for( computerPlayer )
        if winComputer:
            return winComputer
        self.strategy_log("not wincomputer")

        winPlayer = self.compute_move_win_for( humanPlayer )
        if winPlayer:
            return winPlayer
        self.strategy_log("not winplayer");

        forkComputer = this.compute_move_forks_for( computerPlayer )
        if forkComputer:
            return forkComputer
        self.strategy_log("not forkcomputer")

        forkPlayer = this.compute_block_fork_move( humanPlayer, computerPlayer )
        if forkPlayer:
            return forkPlayer
        self.strategy_log("not forkPlayer");

        center = [1, 1];
        if (self.is_cell_empty(center[0], center[1])):
            return center;

        self.strategy_log("not center");

        oppositeCorner = this.find_opposite_corner_move( humanPlayer );
        if oppositeCorner:
            return oppositeCorner
        self.strategy_log("not oppositecorner");

        randomCorner = this.find_first_empty_corner();
        if randomCorner:
            return randomCorner
        self.strategy_log("not randomcorner");

        randomSide = this.find_first_empty_side()
        if randomSide:
            return randomSide
        self.strategy_log("not randomsize");

        console.log("ERROR: Programmer error");
        return [ -1, -1 ];
        

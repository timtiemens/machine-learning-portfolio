#!/usr/bin/env python3

from enum import Enum
import random
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
        if self.value == 1:
            return 0.0
        elif self.value == 2:
            return 1.0
        elif self.value == 3:
            return 2.0
    
    def __str__(self):
        if self.value == 1:
            return '-'
        elif self.value == 2:
            return 'x'
        elif self.value == 3:
            return 'o'
        else:
            print(f" CellValue.value={self.value} failed")
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

    def print_state(self):
        for r in range(3):
            sep = ""
            for c in range(3):
                print(sep, self.get_cell_rowcol(r, c), end="")
                sep = " "
            print("")
    def to_board_array(self, positive_for_player=CellValue.X):
        rtn = []
        winner = self.get_winner()
        if not winner:
            posnegnone = "none"
        else:
            if winner == positive_for_player:
                posnegnone = "positive"
            else:
                posnegnone = "negative"
            
        for r in range(3):
            for c in range(3):
                rtn.append( self.get_cell_rowcol(r, c) )
        rtn.append(posnegnone)
                
        return rtn
                    
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
        if not isinstance(rowcol_one, list):
            raise Exception("rowcol_one must be an array")
        if not isinstance(rowcol_two, list):
            raise Exception("rowcol_two must be an array")
        if len(rowcol_one) != len(rowcol_two):
            raise Exception(f"lengths must be the same {len(rowcol_one)} and {len(rowcol_two)}")
        for v1, v2 in zip(rowcol_one, rowcol_two):
            if (v1 != v2):
                return False
        return True

    def find_matching_move(self, find_row_column: list[int], list_row_columns: list[int]) -> bool:
        if not isinstance(find_row_column, list):
            raise Exception("find_row_column must be an array")
        if not isinstance(list_row_columns, list):
            raise Exception("list_row_columns must be an array")
        for i in range(len(list_row_columns)):
            target = list_row_columns[i]
            if (self.compare_moves(find_row_column, target)):
                return True
        return False

    def check_player_throw(self, player):
        if player is None or not player:
            raise Exception("Must supply non-null 'player' argument")

    # TODO: rename -- this returns [r,c] list of cells that are EMPTY
    def list_empty(self):
        rtn = []
        for r in range(3):
            for c in range(3):
                if self.is_cell_empty(r, c):
                    rtn.append( [r, c] )
        return rtn


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
        for move in items:
            if self.does_move_win_for(player, move):
                rtn.append(move)
        return rtn

    def does_move_win_for(self, player, move_row_column):
        self.check_player_throw(player)
        testboard = Board(self.board)
        testboard.set_cell(move_row_column[0], move_row_column[1], player)
        originalEmpty = self.list_empty()
        nowEmpty = self.list_empty()
        winner = testboard.get_winner()
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
            testboard = Board(self.board)
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
        return self.find_first_empty(Board.sides)

    def find_first_empty(self, moves):
        rtn = None
        for i in range(len(moves)):
            move = moves[i]
            if ((rtn is None) and (self.is_cell_empty(move[0], move[1]))):
                rtn = move
        return rtn

    def find_opposite_corner_move(self, player):
        print(f" enter find_opposite_corner_move  player={player}  type={type(player)}")
        self.check_player_throw(player)
        rtn = None
        for move in Board.corners:
            print(f"find_opp  move={move}")
            if self.get_cell_rowcol(move[0], move[1]) == player:
                print(f"  matched player={player} at {move}")
                opposite = self.get_opposite_rowcol(move)
                print(f"  opposite is_empty {opposite} is {self.is_cell_empty(opposite[0], opposite[1])}")
                if self.is_cell_empty(opposite[0], opposite[1]):
                    rtn = [ opposite[0], opposite[1] ]
        print(f" exit find_opposite rtn={rtn}")
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
                winner = candidate_set.pop()
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

        forkComputer = self.compute_move_forks_for( computerPlayer )
        if forkComputer:
            return forkComputer
        self.strategy_log("not forkcomputer")

        forkPlayer = self.compute_block_fork_move( humanPlayer, computerPlayer )
        if forkPlayer:
            return forkPlayer
        self.strategy_log("not forkPlayer");

        center = [1, 1];
        if (self.is_cell_empty(center[0], center[1])):
            return center;

        self.strategy_log("not center");

        oppositeCorner = self.find_opposite_corner_move( humanPlayer );
        if oppositeCorner:
            return oppositeCorner
        self.strategy_log("not oppositecorner");

        randomCorner = self.find_first_empty_corner();
        if randomCorner:
            return randomCorner
        self.strategy_log("not randomcorner");

        randomSide = self.find_first_empty_side()
        if randomSide:
            return randomSide
        self.strategy_log("not randomsize");

        console.log("ERROR: Programmer error");
        return [ -1, -1 ];
        

class Game:
    
    def __init__(self, the_first_player, the_second_player):
        self.first_player = the_first_player
        self.second_player = the_second_player
        self.current_player = the_first_player
        self.computer_skill = 'First'
        self.game_winner = None
        self.board = Board(None)
        self.strategies = {
            # TODO: remove redundant "_empty"
            'First' : { 'mover' : self.move_first_empty },
            'Random': { 'mover' : self.move_random_empty },
            'Best'  : { 'mover' : self.move_best_empty },
            'Perfect':{ 'mover' : self.move_perfect_empty }
        }
        self.player_to_strategy = {
            the_first_player: 'Random',
            the_second_player: 'Best'
        }

    def copy(other_game):
        game = Game(other_game.first_player, other_game.second_player)
        #print(f"other_game.board={other_game.board.board}       type={type(other_game.board.board)}")
        game.board = Board(other_game.board.board)
        game.current_player = other_game.current_player
        game.computer_skill = other_game.computer_skill
        game.player_to_strategy = other_game.player_to_strategy   # TODO: COPY()
        # TODO: copy(other_game.player_to_strategy)
        return game
        
    def from_indexes(index_array, the_first_player = CellValue.X, the_second_player = CellValue.O):
        game = Game(the_first_player, the_second_player)
        for index in index_array:
            if game.get_game_winner() == None:
                r = int( index / 3 )
                c = index - (r * 3)
                game.player_makes_move(r, c, game.current_player)
            else:
                raise Exception(f"Create game index={index} game_winner already {game.get_game_winner()}")
        return game

    def get_board(self):
        return self.board

    def get_strategy_for_player(self, use_player):
        strategy_name = self.player_to_strategy[use_player]
        return self.strategies[strategy_name]

    def player_makes_move(self, row, col, the_player):
        self.board.set_cell(row, col, the_player)
        self.check_game()
        if (not self.game_winner):
            self.current_player = self.next_player(the_player)

    def next_player(self, from_player):
        if from_player == CellValue.X:
            return CellValue.O
        else:
            return CellValue.X

    def new_game(self):
        board.clear_all_cells()
        self.game_winner = None
        self.current_player = self.first_player
    def check_game(self):
        win = self.board.get_winner()
        count = self.board.count_empty()
        any_empty = count > 0

        if (not win and not any_empty):
            self.game_winner = "NONE"
        else:
            if win:
                self.game_winner = win

    def do_a_turn(self):
        self.do_a_turn_following_strategy(self.get_strategy_for_player(self.current_player))

    def do_a_turn_following_strategy(self, strategy):
        #print(f"datfs strategy={strategy}")
        print(f"do a turn, current={self.current_player}")
        use_player = self.current_player
        other_player = self.next_player(use_player)
        move = strategy['mover'](use_player, other_player)
        self.player_makes_move(move[0], move[1], use_player)
    
    #
    # Strategies - all return [row,col]
    #
    def move_random_empty(self, use_player, other_player):
        # does not use either player to decide:
        items = self.board.list_empty()
        return random.choice(items)

    def move_first_empty(self, use_player, other_player):
        # does not use either player to decide:
        items = self.board.list_empty()
        return items[0]

    def move_best_empty(self, use_player, other_player):
        # Take the win, if available
        # Block the win, if other_player has one
        # Otherwise, take the first available EMPTY cell in ranked order of preference
        
        winUse = self.board.compute_move_win_for( use_player )
        if winUse:
            return winUse
        # self.log("No win for computer");

        winOther = self.board.compute_move_win_for( other_player )
        if winOther:
            return winOther     # block win
        # self.log("No win for human");

        rtn = None
        prefCells = [
                [1, 1],
                [0, 0], [0, 2], [2, 0], [2, 2],
                [0, 1],
                [1, 0], [1, 2],
                [2, 1] ]
        for move in prefCells:
            r = move[0];
            c = move[1];
            if (self.board.is_cell_empty(r, c)):
                rtn =  move;
                break;
        return rtn;        

    def move_perfect_empty(self, use_player, other_player):
        return self.board.strategy_perfect(use_player, other_player)

    # Proxy
    def get_board_winner(self):
        # NOTE: board.get_winner() does not detect "DRAW" - it just returns None
        return self.board.get_winner()

    def get_game_winner(self):
        return self.game_winner
    
    def print_state(self):
        self.board.print_state()

def run_game():
    game = Game(CellValue.O, CellValue.X)
    while game.get_game_winner() == None:
        game.do_a_turn()
        game.print_state()
    print(f"Winner is {game.get_game_winner()}")

def create_all_games_recursive(start_games, finished_games):
    if len(start_games) <= 0:
        print(f"Len start_games is 0")
        return False

    
    game = start_games.pop(0)
    
    if (game.get_game_winner() == None):
        items = game.get_board().list_empty()
        for move in items:
            copy_game = Game.copy(game)
            copy_game.player_makes_move(move[0], move[1], copy_game.current_player)
            winner = copy_game.get_game_winner()
            if (winner == None):
                start_games.insert(0, copy_game)
            else:
                # regardless of if the winner is "NONE" or X or O,
                #  this is a "dead" game:
                finished_games.append(copy_game)
    else:
        print(f"Just pulled a non-None game from start_games")
        # TODO: decide if bug or not:
        finished_games.append(game)

    return len(start_games) != 0

        
        
def create_all_games():
    rtn = []
    if False:
        game = Game.from_indexes([6, 4, 1, 5, 3, 7, 2, 8, 0])
        rtn.append(game)
        print(f"Game 1 - game_winner={game.get_game_winner()}")
        game.print_state()
    else:
        seeds = []   # games with the first move
        for index in range(0, 9):
            game = Game.from_indexes( [index] )
            seeds.append(game)


        for start_game in seeds:
            start_games = [ start_game ]
            finished_games = []
            keep_going  = True
            while keep_going:
                keep_going = create_all_games_recursive( start_games, finished_games)
                rtn.extend(finished_games)
                print(f"Just added {len(finished_games)}  start_games={len(start_games)} rtn={len(rtn)}")
                finished_games = []                
            
    
    return rtn

def write_all_games(all_games, outfile):
    """
      0    1    2    3    4    5    6    7    8
    "V1","V2","V3","V4","V5","V6","V7","V8","V9","V10"
    "x", "x", "x", "x", "o", "o", "x", "o", "o","positive"
    The "simple just add" version creates a file with 255,169 lines.
    This version filters out the duplicates and sorts
    After creating the ttt-endgame.csv file,
    There are no differences between it and the sorted Kaggle .csv file.
    """
    headers = [ "V" + str(i) for i in range(1,11)]
    quote = '"'

    sep = ""
    for col in headers:
        outfile.write(sep + quote + col + quote)
        sep = ","
    outfile.write("\n")

    outlines = set()
    for game in all_games:
        board = game.get_board()
        board_array = board.to_board_array()
        board_array_quotes = [ quote + str(i) + quote for i in board_array ]
        line = ",".join(board_array_quotes)
        line = line.replace("-", "b")
        line = line.replace("none", "negative")
        outlines.add(line)

    listlines = []
    listlines.extend(outlines)
    listlines.sort()
    for line in listlines:
        outfile.write(line + "\n")

    
if __name__ == '__main__':
    if False:
        run_game()
    if True:
        all_games = create_all_games()
        
        with open("ttt-endgame.csv", "w") as outfile:
            write_all_games(all_games, outfile)
            

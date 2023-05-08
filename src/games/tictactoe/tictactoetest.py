
#
# $ pytest -q tictactoetest.py
#


from tictactoe import CellValue, Board

X = 2   #  TODO:  X = CellValue.X ?
O = 3
X = CellValue.X
O = CellValue.O

class TestTicTacToe:
    
    def test_empty_winner(self):
        board = Board(None)
        winner = board.get_winner()
        assert board.get_winner() is None
    def test_opposite(self):
        board = Board(None)
        assert board.is_cell_empty(0,0) == True
        assert board.get_opposite_index(2) == 0  
        assert board.get_opposite_index(1) == 1
        assert board.get_opposite_index(0) == 2
#        assert (board.opposite( [0,0] )[0], 2, "opposite([0,0])" );
#        assert (board.opposite( [0,0] )[1], 2, "opposite([0,0])" );        

    def test_emptycorner(self):
        board = Board(None)
        assert board.find_first_empty_corner() == [0, 0]
        board.set_cell(0, 0, X)
        assert board.find_first_empty_corner() == [0, 2]
        assert board.find_opposite_corner_move(X) == [2, 2]

    def test_emptyside(self):
        board = Board(None)
        assert board.find_first_empty_side() == [0,1]
        board.set_cell(0, 1, X);
        assert board.find_first_empty_side() == [1,0]
        board.set_cell(1, 0, X);
        assert board.find_first_empty_side() == [1,2]
        board.set_cell(1, 2, X);
        assert board.find_first_empty_side() == [2,1]

    def test_samemove(self):
        board = Board(None)
        assert board.compare_moves( [0, 0], [1, 1]) == False
        assert board.compare_moves( [0, 0], [0, 0]) == True
        assert board.compare_moves( [1, 1], [1, 1]) == True

    def test_findmove(self):
        board = Board(None)
        testlist = [ [0, 1], [1, 2] ]
        assert board.find_matching_move( [0, 0], testlist) == False
        assert board.find_matching_move( [0, 1], testlist) == True
        assert board.find_matching_move( [0, 2], testlist) == False
        assert board.find_matching_move( [1, 2], testlist) == True
        
    def test_perfectblockers(self):
        board = Board(None)
        board.set_cell(0, 2, O)
        board.set_cell(1, 1, X)
##        board.set_cell(2, 0, O)  ## TODO: previous test set both corners
        print(f"perfectblocker start")
        assert board.find_opposite_corner_move(O) == [2,0]
        # very hard to get strategy to agree:
        # assert board.strategy_perfect(X, O) == [0, 2]


    # end of original unit tests

    

#
# $ pytest -q tictactoetest.py
#
#if __name__ == '__main__':
#    unittest.main()
    

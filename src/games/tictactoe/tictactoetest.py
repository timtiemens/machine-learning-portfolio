#import uniittest

from tictactoe import Board

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
        board.set_cell(0, 0, 1)
        assert board.find_first_empty_corner() == [0, 2]
        assert board.find_opposite_corner_move(1) == [2, 2]
        

#
# $ pytest -q tictactoetest.py
#
#if __name__ == '__main__':
#    unittest.main()
    

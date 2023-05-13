
#
# $ pytest -q tictactoetest.py
#

import numpy as np


from tictactoe import CellValue, Board

from tictactoe import NineSymmetry

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

    def test_indexflip(self):
        ninesym = NineSymmetry()
        orig = [0,1,2,3,4,5,6,7,8]
        blank = [-1,-1,-1,-1,-1,-1,-1,-1,-1]

        copyin = orig.copy()
        output = blank.copy()
        ninesym.sym_horizontal.transform(copyin, output)
        assert orig == [0,1,2,3,4,5,6,7,8]
        assert copyin == [0,1,2,3,4,5,6,7,8]
        assert output == [2,1,0,  5,4,3,  8,7,6]

        output = blank.copy()
        ninesym.sym_vertical.transform(copyin, output)
        assert output == [6,7,8, 3,4,5, 0,1,2]

        output = blank.copy()
        ninesym.sym_lr_diag.transform(copyin, output)
        assert output == [8,5,2, 7,4,1, 6,3,0]

        output = blank.copy()
        ninesym.sym_rl_diag.transform(copyin, output)
        assert output == [0,3,6, 1,4,7, 2,5,8]
        
    def test_transform_individuals(self):
        ninesym = NineSymmetry()
        orig = [0,1,2,3,4,5,6,7,8]
        blank = [-1,-1,-1,-1,-1,-1,-1,-1,-1]

        copyin = orig.copy()
        output = blank.copy()
        ninesym.tc_horizontal.transform(copyin, output)
        assert orig == [0,1,2,3,4,5,6,7,8]
        assert copyin == [0,1,2,3,4,5,6,7,8]
        assert output == [2,1,0,  5,4,3,  8,7,6]

        output = blank.copy()
        ninesym.tc_vertical.transform(copyin, output)
        assert output == [6,7,8, 3,4,5, 0,1,2]

        output = blank.copy()
        ninesym.tc_lrdiag.transform(copyin, output)
        assert output == [8,5,2, 7,4,1, 6,3,0]

        output = blank.copy()
        ninesym.tc_rldiag.transform(copyin, output)
        assert output == [0,3,6, 1,4,7, 2,5,8]
        

    def test_transform_combinations(self):        
        ninesym = NineSymmetry()
        orig = [0,1,2,3,4,5,6,7,8]
        blank = [-1,-1,-1,-1,-1,-1,-1,-1,-1]

        copyin = orig.copy()
        output = blank.copy()
        ninesym.tc_hor_vert.transform(copyin, output)
        assert output == [8,7,6, 5,4,3, 2,1,0]

        # vert_hor is the same as hor_vert:
        copyin = orig.copy()
        output = blank.copy()
        ninesym.tc_vert_hor.transform(copyin, output)
        assert output == [8,7,6, 5,4,3, 2,1,0]
        
        
    def test_symmetry(self):
        ninesym = NineSymmetry()
        npnine = np.array([0,1,2,3,4,5,6,7,8])
        print(f"Orig        = {npnine}")

        flipupd = np.flipud(  np.reshape(npnine, (3,3))  ).flatten()
        print(f"np.FlipUpd  = {flipupd}")
        print(f"NS.sym_vert = {ninesym.sym_vertical}")

        fliplr = np.fliplr(  np.reshape(npnine, (3,3))  ).flatten()
        print(f"np.FlipLr   = {fliplr}")
        print(f"NS.sym_hori = {ninesym.sym_horizontal}")
        
        print(f"END TEST_SYMMETRIC")

    def test_compute_all_unique(self):
        ninesym = NineSymmetry()
        output2transform = ninesym.compute_all_unique()
        # 1 "identity" transform plus 7 other unique transforms:
        assert len(output2transform.keys()) == 8
#
# $ pytest -q -rP tictactoetest.py
#
#if __name__ == '__main__':
#    unittest.main()
    

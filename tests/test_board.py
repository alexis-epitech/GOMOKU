
import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from game.board import Board

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board(20)

    def test_horizontal_win(self):
        for i in range(5):
            self.board.place_stone(10 + i, 10, 1)
        self.assertTrue(self.board.check_win(1))

    def test_vertical_win(self):
        for i in range(5):
            self.board.place_stone(10, 10 + i, 1)
        self.assertTrue(self.board.check_win(1))
    
    def test_diagonal_win(self):
        for i in range(5):
            self.board.place_stone(10 + i, 10 + i, 1)
        self.assertTrue(self.board.check_win(1))

    def test_no_win_on_4(self):
        for i in range(4):
            self.board.place_stone(10 + i, 10, 1)
        self.assertFalse(self.board.check_win(1))

    def test_undo_mechanic(self):
        self.board.place_stone(10, 10, 1)
        success = self.board.place_stone(10, 10, 0)
        self.assertTrue(success, "Should be able to remove move without force=True (Bug?)")
        self.assertEqual(self.board.grid[10][10], 0)

    def test_occupied_cells_missing(self):
        self.assertFalse(hasattr(self.board, 'occupied_cells'), "Board should NOT have occupied_cells (as requested)")

if __name__ == '__main__':
    unittest.main()


import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from game.board import Board
from ai.patterns import PatternDetector

class TestPatternDetector(unittest.TestCase):
    def setUp(self):
        self.board = Board(20)
        self.detector = PatternDetector(self.board)

    def test_detect_five(self):
        for i in range(4):
            self.board.place_stone(10 + i, 10, 1)
        threats = self.detector.analyze_move(14, 10, 1)
        self.assertEqual(threats['five'], 1, "Should detect a Five")

    def test_detect_open_four(self):
        for i in range(1, 4):
            self.board.place_stone(10 + i, 10, 1)
        threats = self.detector.analyze_move(14, 10, 1)
        self.assertEqual(threats['open_four'], 1, "Should detect Open Four")

    def test_detect_blocked_four(self):
        self.board.place_stone(9, 10, 2)
        for i in range(3):
            self.board.place_stone(10 + i, 10, 1)
        threats = self.detector.analyze_move(13, 10, 1)
        self.assertEqual(threats['four'], 1, "Should detect Blocked Four")
        self.assertEqual(threats['open_four'], 0, "Should NOT detect Open Four")

    def test_detect_running_three(self):
        self.board.place_stone(10, 10, 1)
        self.board.place_stone(11, 10, 1)
        threats = self.detector.analyze_move(12, 10, 1)
        self.assertEqual(threats['open_three'], 1, "Should detect Open Three")

    def test_detect_gap_four(self):
        self.board.place_stone(10, 10, 1)
        self.board.place_stone(11, 10, 1)
        self.board.place_stone(13, 10, 1)
        
        threats = self.detector.analyze_move(12, 10, 1)
        self.assertEqual(threats['open_four'], 1, "Should detect Open Four filling a gap")
    
    def test_detect_split_three(self):
        self.board.place_stone(10, 10, 1)
        self.board.place_stone(12, 10, 1)
        threats = self.detector.analyze_move(11, 10, 1)
        self.assertEqual(threats['open_three'], 1, "Fill gap to make 3")

    def test_double_counting_bug(self):
        self.board.place_stone(9, 10, 2)
        self.board.place_stone(10, 10, 1)
        self.board.place_stone(11, 10, 1)
        self.board.place_stone(12, 10, 1)
        
        threats = self.detector.analyze_move(13, 10, 1)
        
        self.assertEqual(threats['four'], 1, "Should detect exactly one Four")
        self.assertEqual(threats['open_three'], 0, "Should NOT detect Open Three (double count bug)")

if __name__ == '__main__':
    unittest.main()

from __future__ import annotations
from game.board import Board


class PatternDetector:
    def __init__(self, board: Board):
        self.board = board
        self.directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    def analyze_move(
        self, x: int, y: int, player: int
    ) -> dict[str, int]:
        """Analyze a single move quickly"""
        threats = {
            "five": 0,
            "open_four": 0,
            "four": 0,
            "open_three": 0,
            "two": 0,
        }

        opponent = 3 - player
        self.board.grid[y][x] = player

        for dx, dy in self.directions:
            count = 1
            open_left = False
            open_right = False

            left_count = 0
            i = 1
            while True:
                nx, ny = x - i * dx, y - i * dy
                if not (0 <= nx < self.board.size and 0 <= ny < self.board.size):
                    break
                if self.board.grid[ny][nx] == player:
                    left_count += 1
                    i += 1
                elif self.board.grid[ny][nx] == 0:
                    open_left = True
                    break
                else:
                    break

            right_count = 0
            i = 1
            while True:
                nx, ny = x + i * dx, y + i * dy
                if not (0 <= nx < self.board.size and 0 <= ny < self.board.size):
                    break
                if self.board.grid[ny][nx] == player:
                    right_count += 1
                    i += 1
                elif self.board.grid[ny][nx] == 0:
                    open_right = True
                    break
                else:
                    break

            count = 1 + left_count + right_count

            if count >= 5:
                threats["five"] += 1
            elif count == 4:
                if open_left and open_right:
                    threats["open_four"] += 1
                elif open_left or open_right:
                    threats["four"] += 1
            elif count == 3:
                if open_left and open_right:
                    threats["open_three"] += 1
            elif count == 2:
                if open_left or open_right:
                    threats["two"] += 1

            if count < 5:
                gap_pattern = self._check_gap_pattern(x, y, dx, dy, player)
                if gap_pattern == 4:
                    threats["four"] += 1
                elif gap_pattern == 3:
                    threats["open_three"] += 1

        self.board.grid[y][x] = 0
        return threats

    def _check_gap_pattern(self, x: int, y: int, dx: int, dy: int, player: int) -> int:
        """Check for patterns with one gap like XX.X"""
        for start in range(-4, 1):
            stones = 0
            gap_pos = -1
            has_gap = False
            blocked = 0

            for i in range(5):
                nx, ny = x + (start + i) * dx, y + (start + i) * dy
                if not (0 <= nx < self.board.size and 0 <= ny < self.board.size):
                    blocked += 1
                    continue

                cell = self.board.grid[ny][nx]
                if cell == player:
                    stones += 1
                elif cell == 0:
                    if has_gap:
                        break
                    has_gap = True
                    gap_pos = i
                else:
                    blocked += 1

            if stones == 4 and has_gap and blocked == 0:
                return 4
            elif stones == 3 and has_gap and blocked == 0:
                return 3

        return 0

    def find_critical_moves(self, player: int) -> list[tuple[int, int, int]]:
        """Find critical moves with scores (faster)"""
        moves = []
        opponent = 3 - player

        for y in range(self.board.size):
            for x in range(self.board.size):
                if self.board.grid[y][x] != 0:
                    continue

                if not self._is_near_stone(x, y, 2):
                    continue

                my_score = self._quick_score(x, y, player)
                opp_score = self._quick_score(x, y, opponent)

                score = my_score * 2 + opp_score
                if score > 0:
                    moves.append((x, y, score))

        moves.sort(key=lambda m: m[2], reverse=True)
        return moves[:15]

    def _is_near_stone(self, x: int, y: int, dist: int) -> bool:
        """Check if near any stone"""
        for dy in range(-dist, dist + 1):
            for dx in range(-dist, dist + 1):
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < self.board.size
                    and 0 <= ny < self.board.size
                    and self.board.grid[ny][nx] != 0
                ):
                    return True
        return False

    def _quick_score(self, x: int, y: int, player: int) -> int:
        """Quick scoring for move ordering"""
        threats = self.analyze_move(x, y, player)
        score = 0
        score += threats["five"] * 100000
        score += threats["open_four"] * 10000
        score += threats["four"] * 1000
        score += threats["open_three"] * 500
        score += threats["two"] * 10
        return score
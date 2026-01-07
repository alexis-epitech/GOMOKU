# ai/minimax.py
from __future__ import annotations
from copy import deepcopy
from game.board import Board


class MinimaxAI:
    def __init__(self, depth: int = 2):
        self.max_depth = depth

    def evaluate(self, board: Board, player: int) -> int:
        opponent = 1 if player == 2 else 2

        def count_lines(p: int, length: int) -> int:
            count = 0
            n = board.size
            for y in range(n):
                for x in range(n):
                    if board.grid[y][x] != p:
                        continue
                    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
                    for dx, dy in directions:
                        if (
                            all(
                                0 <= x + k * dx < n
                                and 0 <= y + k * dy < n
                                and board.grid[y + k * dy][x + k * dx] == p
                                for k in range(length)
                            )
                            and (x - dx < 0 or board.grid[y - dy][x - dx] != p)
                            and (
                                x + length * dx >= n
                                or y + length * dy >= n
                                or board.grid[y + length * dy][x + length * dx] != p
                            )
                        ):
                            count += 1
            return count

        def score_lines(p: int) -> int:
            weights = {2: 5, 3: 50, 4: 500, 5: 100000}
            return sum(count_lines(p, l) * weights[l] for l in weights)

        return score_lines(player) - score_lines(opponent)

    def minimax(
        self, board: Board, depth: int, maximizing: bool, player: int
    ) -> tuple[int, tuple[int, int] | None]:
        opponent = 1 if player == 2 else 2

        if depth == 0 or board.check_win(player) or board.check_win(opponent):
            return self.evaluate(board, player), None

        moves = self.possible_moves(board)
        if not moves:
            return self.evaluate(board, player), None

        if maximizing:
            best_score = -10**9
            best_move = None
            for (x, y) in moves:
                new_board = deepcopy(board)
                new_board.place_stone(x, y, player)
                score, _ = self.minimax(new_board, depth - 1, False, player)
                if score > best_score:
                    best_score = score
                    best_move = (x, y)
            return best_score, best_move
        else:
            best_score = 10**9
            best_move = None
            for (x, y) in moves:
                new_board = deepcopy(board)
                new_board.place_stone(x, y, opponent)
                score, _ = self.minimax(new_board, depth - 1, True, player)
                if score < best_score:
                    best_score = score
                    best_move = (x, y)
            return best_score, best_move

    def possible_moves(self, board: Board) -> list[tuple[int, int]]:
        n = board.size
        moves = set()
        for y in range(n):
            for x in range(n):
                if board.grid[y][x] != 0:
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            nx, ny = x + dx, y + dy
                            if (
                                0 <= nx < n
                                and 0 <= ny < n
                                and board.grid[ny][nx] == 0
                            ):
                                moves.add((nx, ny))
        if not moves:
            moves.add((n // 2, n // 2))
        return list(moves)

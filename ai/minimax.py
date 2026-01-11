from __future__ import annotations
from game.board import Board
from ai.patterns import PatternDetector


class MinimaxAI:
    def __init__(self, depth: int = 2):
        self.max_depth = depth

    def evaluate(self, board: Board, player: int) -> int:
        """Fast evaluation"""
        score = 0
        opponent = 3 - player

        for y in range(board.size):
            for x in range(board.size):
                cell = board.grid[y][x]
                if cell == player:
                    score += self._position_value(board, x, y, player)
                elif cell == opponent:
                    score -= self._position_value(board, x, y, opponent)

        return score

    def _position_value(
        self, board: Board, x: int, y: int, player: int
    ) -> int:
        """Fast position evaluation"""
        value = 0
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for dx, dy in directions:
            count = 1
            # Count in both directions
            for d in [-1, 1]:
                i = 1
                while True:
                    nx, ny = x + i * dx * d, y + i * dy * d
                    if not (0 <= nx < board.size and 0 <= ny < board.size):
                        break
                    if board.grid[ny][nx] == player:
                        count += 1
                        i += 1
                    else:
                        break

            if count >= 5:
                value += 100000
            elif count == 4:
                value += 10000
            elif count == 3:
                value += 1000
            elif count == 2:
                value += 100

        return value

    def minimax(
        self,
        board: Board,
        depth: int,
        alpha: float,
        beta: float,
        maximizing: bool,
        player: int,
    ) -> tuple[float, tuple[int, int] | None]:
        """Minimax with alpha-beta (no deepcopy!)"""
        opponent = 3 - player

        if depth == 0:
            return self.evaluate(board, player), None

        if board.check_win(player):
            return 100000 + depth * 1000, None
        if board.check_win(opponent):
            return -100000 - depth * 1000, None

        # Get candidate moves
        detector = PatternDetector(board)
        candidates = detector.find_critical_moves(player)

        if not candidates:
            return self.evaluate(board, player), None

        best_move = None

        if maximizing:
            max_score = -float("inf")
            for x, y, _ in candidates[:10]:  # Top 10 only
                # Make move
                board.grid[y][x] = player
                score, _ = self.minimax(
                    board, depth - 1, alpha, beta, False, player
                )
                # Undo move
                board.grid[y][x] = 0

                if score > max_score:
                    max_score = score
                    best_move = (x, y)

                alpha = max(alpha, score)
                if beta <= alpha:
                    break

            return max_score, best_move
        else:
            min_score = float("inf")
            for x, y, _ in candidates[:10]:
                # Make move
                board.grid[y][x] = opponent
                score, _ = self.minimax(
                    board, depth - 1, alpha, beta, True, player
                )
                # Undo move
                board.grid[y][x] = 0

                if score < min_score:
                    min_score = score
                    best_move = (x, y)

                beta = min(beta, score)
                if beta <= alpha:
                    break

            return min_score, best_move

    def find_best_move(
        self, board: Board, player: int
    ) -> tuple[int, int] | None:
        """Find best move"""
        _, move = self.minimax(
            board, self.max_depth, -float("inf"), float("inf"), True, player
        )
        return move
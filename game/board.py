
class Board:
    def __init__(self, size: int = 20):
        self.size = size
        self.grid: list[list[int]] = [[0 for _ in range(size)] for _ in range(size)]

    def clear(self) -> None:
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]

    def is_valid_move(self, x: int, y: int) -> bool:
        return 0 <= x < self.size and 0 <= y < self.size and self.grid[y][x] == 0

    def place_stone(self, x: int, y: int, player: int, force: bool = False) -> bool:
        if not (0 <= x < self.size and 0 <= y < self.size):
            return False
        if not force and not self.is_valid_move(x, y):
            return False
        self.grid[y][x] = player
        return True

    def count_consecutive(self, x: int, y: int, dx: int, dy: int, player: int) -> int:
        count = 0
        i, j = x + dx, y + dy
        while 0 <= i < self.size and 0 <= j < self.size and self.grid[j][i] == player:
            count += 1
            i += dx
            j += dy
        return count

    def check_win(self, player: int) -> bool:
        n = self.size
        for y in range(n):
            for x in range(n):
                if self.grid[y][x] != player:
                    continue
                if x <= n - 5 and all(self.grid[y][x + k] == player for k in range(5)):
                    return True
                if y <= n - 5 and all(self.grid[y + k][x] == player for k in range(5)):
                    return True
                if (x <= n - 5 and y <= n - 5 and all(self.grid[y + k][x + k] == player for k in range(5))):
                    return True
                if (x <= n - 5 and y >= 4 and all(self.grid[y - k][x + k] == player for k in range(5))):
                    return True
        return False

    def check_win_in_1(self, player: int) -> list[tuple[int, int]]:
        moves = []
        for y in range(self.size):
            for x in range(self.size):
                if not self.is_valid_move(x, y):
                    continue
                self.grid[y][x] = player
                if self.check_win(player):
                    moves.append((x, y))
                self.grid[y][x] = 0
        return moves

    def check_lose_in_1(self, player: int) -> list[tuple[int, int]]:
        opponent = 1 if player == 2 else 2
        return self.check_win_in_1(opponent)

    def check_win_in_2(self, player: int) -> list[tuple[int, int]]:
        moves = []
        dirs = [(1, 0), (0, 1), (1, 1), (1, -1)]
        n = self.size
        for y in range(n):
            for x in range(n):
                if not self.is_valid_move(x, y):
                    continue
                self.grid[y][x] = player
                for dx, dy in dirs:
                    left = self.count_consecutive(x, y, -dx, -dy, player)
                    right = self.count_consecutive(x, y, dx, dy, player)
                    total = 1 + left + right
                    if total >= 3:
                        lx, ly = x - (left + 1) * dx, y - (left + 1) * dy
                        rx, ry = x + (right + 1) * dx, y + (right + 1) * dy
                        open_left = 0 <= lx < n and 0 <= ly < n and self.grid[ly][lx] == 0
                        open_right = (0 <= rx < n and 0 <= ry < n and self.grid[ry][rx] == 0)
                        if open_left or open_right:
                            moves.append((x, y))
                            break
                self.grid[y][x] = 0
        return moves

    def check_lose_in_2(self, player: int) -> list[tuple[int, int]]:
        opponent = 1 if player == 2 else 2
        return self.check_win_in_2(opponent)

    def __str__(self) -> str:
        symbols = {0: ".", 1: "X", 2: "O"}
        return "\n".join(" ".join(symbols[c] for c in row) for row in self.grid)

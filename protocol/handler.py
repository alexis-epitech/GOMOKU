class ProtocolHandler:
    def __init__(self):
        self.should_exit = False
        self.board_size: int = 0
        self.board: list[list[int]] | None = None
        self.ready: bool = False

    def process(self, line: str) -> str | None:
        parts = line.strip().split()
        if not parts:
            return None
        cmd = parts[0].upper()
        if cmd == "START":
            return self.handle_start(parts)
        elif cmd == "BEGIN":
            return self.handle_begin()
        elif cmd == "TURN":
            return self.handle_turn(parts)
        elif cmd == "BOARD":
            return self.handle_board()
        elif cmd == "END":
            self.should_exit = True
            return None
        return f"UNKNOWN {line}"

    def handle_start(self, parts: list[str]) -> str:
        if len(parts) != 2:
            return "ERROR wrong parameter count"
        size_str = parts[1]
        if not size_str.isdigit():
            return "ERROR invalid parameter"
        size = int(size_str)
        if size < 5 or size > 100:
            return f"ERROR invalid board size {size}"
        self.board_size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.ready = True
        return "OK"

    def handle_begin(self) -> str:
        if not self.ready or self.board is None:
            return "ERROR board not initialized"
        center = self.board_size // 2
        x, y = center, center
        self.board[y][x] = 1
        return f"{x},{y}"

    def handle_turn(self, parts: list[str]) -> str:
        if not self.ready or self.board is None:
            return "ERROR board not initialized"
        if len(parts) != 2 or "," not in parts[1]:
            return "ERROR wrong parameter format"
        try:
            x_str, y_str = parts[1].split(",")
            x, y = int(x_str), int(y_str)
        except ValueError:
            return "ERROR invalid coordinates"
        if not (0 <= x < self.board_size and 0 <= y < self.board_size):
            return "ERROR move out of range"
        if self.board[y][x] != 0:
            return "ERROR cell already occupied"
        self.board[y][x] = 2
        move = self.find_next_move()
        if move is None:
            return "ERROR no valid moves"
        mx, my = move
        self.board[my][mx] = 1
        return f"{mx},{my}"

    def handle_board(self) -> str:
        if not self.ready or self.board is None:
            return "ERROR board not initialized"
        import sys
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            line = line.strip()
            if line.upper() == "DONE":
                break
            try:
                x_str, y_str, field_str = line.split(",")
                x, y, field = int(x_str), int(y_str), int(field_str)
            except ValueError:
                return "ERROR invalid board data"
            if 0 <= x < self.board_size and 0 <= y < self.board_size:
                if field in (1, 2):
                    self.board[y][x] = field
        move = self.find_next_move()
        if move is None:
            return "ERROR no valid moves"
        mx, my = move
        self.board[my][mx] = 1
        return f"{mx},{my}"

    def find_next_move(self) -> tuple[int, int] | None:
        for y in range(self.board_size):
            for x in range(self.board_size):
                if self.board[y][x] == 0:
                    return x, y
        return None
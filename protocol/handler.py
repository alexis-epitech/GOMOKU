from game.board import Board

class ProtocolHandler:
    def __init__(self):
        self.should_exit = False
        self.board: Board | None = None
        self.ready = False
        self.info: dict[str, str] = {}

    def process(self, line: str) -> str | None:
        parts = line.strip().split()
        if not parts:
            return None

        cmd = parts[0].upper()
        if cmd == "START":
            return self.handle_start(parts)
        if cmd == "BEGIN":
            return self.handle_begin()
        if cmd == "TURN":
            return self.handle_turn(parts)
        if cmd == "BOARD":
            return self.handle_board()
        if cmd == "INFO":
            return self.handle_info(parts)
        if cmd == "ABOUT":
            return self.handle_about()
        if cmd == "END":
            self.should_exit = True
            return None
        return f"UNKNOWN {line}"

    def handle_start(self, parts: list[str]) -> str:
        if len(parts) != 2 or not parts[1].isdigit():
            return "ERROR invalid parameters"
        size = int(parts[1])
        if not 5 <= size <= 100:
            return "ERROR invalid board size"
        self.board = Board(size)
        self.ready = True
        return "OK"

    def handle_begin(self) -> str:
        if not self.board:
            return "ERROR board not initialized"
        c = self.board.size // 2
        self.board.place_stone(c, c, 1)
        return f"{c},{c}"

    def handle_turn(self, parts: list[str]) -> str:
        if not self.board:
            return "ERROR board not initialized"
        try:
            x_str, y_str = parts[1].split(",")
            x, y = int(x_str), int(y_str)
        except Exception:
            return "ERROR wrong format"

        if not (0 <= x < self.board.size and 0 <= y < self.board.size):
            return "ERROR invalid move"
        if not self.board.is_valid_move(x, y):
            return "ERROR invalid move"
        self.board.place_stone(x, y, 2, force=True)

        block = self.find_block_move()
        if block:
            bx, by = block
            self.board.place_stone(bx, by, 1)
            return f"{bx},{by}"

        move = self.find_next_move()
        if move is None:
            return "ERROR no valid moves"
        mx, my = move
        self.board.place_stone(mx, my, 1)
        return f"{mx},{my}"

    def handle_board(self) -> str:
        import sys

        if not self.board:
            return "ERROR board not initialized"
        self.board.clear()
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            if line.upper() == "DONE":
                break
            x, y, v = map(int, line.split(","))
            self.board.place_stone(x, y, v, force=True)

        block = self.find_block_move()
        if block:
            bx, by = block
            self.board.place_stone(bx, by, 1)
            return f"{bx},{by}"

        move = self.find_next_move()
        if move is None:
            return "ERROR no valid moves"
        mx, my = move
        self.board.place_stone(mx, my, 1)
        return f"{mx},{my}"

    def handle_board_lines(self, lines: list[str]) -> str:
        if not self.board:
            self.board = Board(20)
            self.ready = True
        self.board.clear()
        for ln in lines:
            if not ln:
                continue
            x, y, v = map(int, ln.split(","))
            self.board.place_stone(x, y, v, force=True)

        block = self.find_block_move()
        if block:
            bx, by = block
            self.board.place_stone(bx, by, 1)
            return f"{bx},{by}"

        move = self.find_next_move()
        if move is None:
            return "ERROR no valid moves"
        mx, my = move
        self.board.place_stone(mx, my, 1)
        return f"{mx},{my}"

    def handle_info(self, parts: list[str]) -> None:
        if len(parts) >= 3:
            self.info[parts[1].lower()] = " ".join(parts[2:])
        return None

    def handle_about(self) -> str:
        return ('name="pbrain-gomoku-ai", version="2.1", author="Raphael Guerin", country="FR"')

    def find_block_move(self) -> tuple[int, int] | None:
        b = self.board
        if not b:
            return None
        threat_moves = b.check_lose_in_1(1)
        if threat_moves:
            threat_moves.sort(key=lambda m: (m[1], m[0]))
            return threat_moves[0]
        return None

    def find_tactical_move(self) -> tuple[int, int] | None:
        b = self.board
        if not b:
            return None

        for method in (b.check_win_in_1, b.check_lose_in_1, b.check_win_in_2, b.check_lose_in_2,):
            moves = method(1)
            if moves:
                moves.sort(key=lambda m: (m[1], m[0]))
                return moves[0]
        return None

    def find_next_move(self) -> tuple[int, int] | None:
        b = self.board
        if not b:
            return None

        if b.check_win(1):
            print("I win!", flush=True)
            self.should_exit = True
            return None
        if b.check_win(2):
            print("You won !", flush=True)
            self.should_exit = True
            return None
        mv = self.find_tactical_move()
        if mv:
            return mv
        for y in range(b.size):
            for x in range(b.size):
                if b.is_valid_move(x, y):
                    return (x, y)
        return None
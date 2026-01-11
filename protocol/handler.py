from ai.minimax import MinimaxAI
from ai.patterns import PatternDetector
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
        if len(parts) < 2:
            return "ERROR wrong format"

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
        move = self.find_best_strategic_move()

        if move is None:
            return "ERROR no valid moves"

        mx, my = move

        # Validate the move is still valid before placing it
        if not self.board.is_valid_move(mx, my):
            # Find fallback move
            detector = PatternDetector(self.board)
            candidates = detector.find_critical_moves(1)
            if candidates:
                mx, my = candidates[0][0], candidates[0][1]
            else:
                return "ERROR no valid moves"

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
            try:
                parts = ln.split(",")
                if len(parts) != 3:
                    continue
                x, y, v = map(int, parts)
                self.board.place_stone(x, y, v, force=True)
            except (ValueError, IndexError):
                continue

        move = self.find_best_strategic_move()
        if move is None:
            c = self.board.size // 2
            return f"{c},{c}"

        mx, my = move
        self.board.place_stone(mx, my, 1)
        return f"{mx},{my}"

    def handle_info(self, parts: list[str]) -> None:
        if len(parts) >= 3:
            self.info[parts[1].lower()] = " ".join(parts[2:])
        return None

    def handle_about(self) -> str:
        return 'name="pbrain-gomoku-ai", version="2.2", author="Raphael Guerin", country="FR"'

    def find_best_strategic_move(self) -> tuple[int, int] | None:
        """Priority-based strategy (fast)"""
        if not self.board:
            return None
    
        detector = PatternDetector(self.board)
    
        # Priority 1: Win immediately
        for y in range(self.board.size):
            for x in range(self.board.size):
                if self.board.grid[y][x] == 0:
                    threats = detector.analyze_move(x, y, 1)
                    if threats["five"] > 0:
                        return (x, y)
    
        # Priority 2: Block opponent win
        for y in range(self.board.size):
            for x in range(self.board.size):
                if self.board.grid[y][x] == 0:
                    threats = detector.analyze_move(x, y, 2)
                    if threats["five"] > 0:
                        return (x, y)
    
        # Priority 3: Block opponent open-4
        for y in range(self.board.size):
            for x in range(self.board.size):
                if self.board.grid[y][x] == 0:
                    threats = detector.analyze_move(x, y, 2)
                    if threats["open_four"] > 0:
                        return (x, y)
    
        # Priority 4: Block opponent four
        for y in range(self.board.size):
            for x in range(self.board.size):
                if self.board.grid[y][x] == 0:
                    threats = detector.analyze_move(x, y, 2)
                    if threats["four"] > 0:
                        return (x, y)
    
        # Priority 5: CREATE OUR OWN FOUR
        for y in range(self.board.size):
            for x in range(self.board.size):
                if self.board.grid[y][x] == 0:
                    threats = detector.analyze_move(x, y, 1)
                    if threats["four"] > 0:
                        return (x, y)
    
        # Priority 6: Create open-4
        for y in range(self.board.size):
            for x in range(self.board.size):
                if self.board.grid[y][x] == 0:
                    threats = detector.analyze_move(x, y, 1)
                    if threats["open_four"] > 0:
                        return (x, y)
    
        # Priority 7: Create multiple open-3s
        best_score = 0
        best_move = None
        for y in range(self.board.size):
            for x in range(self.board.size):
                if self.board.grid[y][x] == 0:
                    threats = detector.analyze_move(x, y, 1)
                    if threats["open_three"] >= 2:
                        return (x, y)
                    score = threats["open_three"] * 100 + threats["four"] * 50
                    if score > best_score:
                        best_score = score
                        best_move = (x, y)
    
        if best_move and best_score > 0:
            return best_move
    
        # Priority 8: Fall back to critical moves
        candidates = detector.find_critical_moves(1)
        if candidates:
            return (candidates[0][0], candidates[0][1])
    
        # Priority 9: Just find ANY empty cell on the board
        for y in range(self.board.size):
            for x in range(self.board.size):
                if self.board.is_valid_move(x, y):
                    return (x, y)
    
        return None
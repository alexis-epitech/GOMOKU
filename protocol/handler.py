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
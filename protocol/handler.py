class ProtocolHandler:
    def __init__(self):
        self.should_exit = False

    def process(self, line: str) -> str | None:
        line = line.strip()
        cmd = line.split()[0].upper()

        if cmd == "END":
            self.should_exit = True
            return None

        return f"UNKNOWN {line}"
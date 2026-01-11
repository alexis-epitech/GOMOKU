# pbrain-gomoku-ai

An advanced AI for the game of Gomoku (Five in a Row), implementing the Piskvork protocol. Designed to compete in Gomocup tournaments.

## Overview

This project implements a Gomoku AI engine using Python. It uses Minimax algorithm with Alpha-Beta pruning, iterative deepening, and heuristic evaluation based on pattern detection (threat search).

**Key Features:**
- **Protocol Compliance**: Fully supports the Piskvork AI protocol (START, TURN, BOARD, BEGIN, INFO, etc.).
- **Minimax AI**: Depth-limited search with Alpha-Beta pruning.
- **Pattern Detection**: Recognition of critical shapes (Open 3, Open 4, Five).
- **Optimization**: Efficient board evaluation and move generation using localized search (checking only relevant neighbors).
- **Resilience**: Robust handling of protocol edge cases (e.g., immediate EOF, delayed pipes).

## Requirements

- **Python 3.10+** (Reason: Uses modern type hinting `|` syntax).
- **OS**: Linux (Target platform), Windows/macOS compatible.

## Installation

No dependencies are required beyond the Python standard library.

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd GOMOKU
   ```

2. Make the script executable:
   ```bash
   chmod +x pbrain-gomoku-ai
   ```

## Usage

### Running as a Standalone executable
The AI is designed to communicate via Standard Input/Output (stdin/stdout). You can run it directly:

```bash
./pbrain-gomoku-ai
```

Then, you can type Piskvork protocol commands.

**Example Session:**
```text
START 20
OK
BEGIN
10,10
TURN 10,11
11,11
BOARD
10,10,1
10,11,2
11,11,1
DONE
9,10
END
```

### Running with Piskvork Manager
To use this AI in the Piskvork GUI or Gomocup manager:
1. Open Piskvork.
2. Go to `Players` -> `Settings` -> `New`.
3. Select the `pbrain-gomoku-ai` script (ensure it is executable).

## Compilation (Windows Executable)
If you need to produce a `.exe` for Windows, you can use PyInstaller:
```bash
pip install pyinstaller
pyinstaller --onefile pbrain-gomoku-ai
```
The executable will be in `dist/`.

## Documentation
- **Protocol Specification**: See [doc/PROTOCOL.md](doc/PROTOCOL.md) for a detailed RFC-style description of the communication protocol.

## Authors
- **Raphael Guerin - raphael.guerin@epitech.eu**
- **Laurent Aliu - laurent.aliu@epitech.eu**
- **Alexis Constantinopoulos - alexis.constantinopoulos@epitech.eu**

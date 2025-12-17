import pytest
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from protocol.handler import ProtocolHandler

def run_board_test(setup_lines: list[str]) -> str:
    handler = ProtocolHandler()
    result = None
    buffer: list[str] = []

    for line in setup_lines:
        if line.startswith("START"):
            handler.process(line)
        elif line == "BOARD":
            buffer = []
        elif line == "DONE":
            result = handler.handle_board_lines(buffer)
        else:
            buffer.append(line)

    return result

def test_win_in_1():
    setup = [
        "START 20",
        "BOARD",
        "5,5,1",
        "6,5,1",
        "7,5,1",
        "8,5,1",
        "DONE",
    ]
    move = run_board_test(setup)
    assert move in ["4,5", "9,5"], f"Expected finishing move, got {move}"


def test_lose_in_1():
    setup = [
        "START 20",
        "BOARD",
        "10,10,2",
        "11,10,2",
        "12,10,2",
        "13,10,2",
        "DONE",
    ]
    move = run_board_test(setup)
    assert move in ["9,10", "14,10"], f"Expected block, got {move}"


def test_win_in_2():
    setup = [
        "START 20",
        "BOARD",
        "4,4,1",
        "5,4,1",
        "7,4,1",
        "DONE",
    ]
    move = run_board_test(setup)
    assert move in ["6,4", "3,4", "8,4"], f"Expected connecting/extension move, got {move}"


def test_lose_in_2():
    setup = [
        "START 20",
        "BOARD",
        "8,8,2",
        "9,8,2",
        "11,8,2",
        "DONE",
    ]
    move = run_board_test(setup)
    assert move in ["10,8", "7,8", "12,8"], f"Expected block move, got {move}"
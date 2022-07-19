
from chupochess.game import game
from chupochess.pieces import king


def penis(inp: int):
    x = game()
    s = ""
    for i in range(inp):
        s += x.data
    return s

def inher(color: str):
    x = king(color)
    return x.print_color()

from chupochess.game import Game
from chupochess.pieces import King
from chupochess.board import Board


def penis(inp: int):
    game = Game()
    s = ""
    for i in range(inp):
        s += game.data
    return s

def inher(color: str):
    king = King(color)
    return king.print_color()
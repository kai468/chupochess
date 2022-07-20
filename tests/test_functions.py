
# run all tests via command line with command "python setup.py pytest" in home folder

from chupochess.pieces import King
from chupochess import functions
from chupochess.game import Game

def test_penis():
    assert functions.penis(3) == "hallohallohallo"

def test_inheritance():
    wK = King("white")
    assert wK.print_color() == "white"


def test_test():
    game = Game()
    game.main()
    
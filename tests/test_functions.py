
# run all tests via command line with command "python setup.py pytest" in home folder

from chupochess.pieces import king
from chupochess import functions

def test_penis():
    assert functions.penis(3) == "hallohallohallo"

def test_inheritance():
    wK = king("white")
    assert wK.print_color() == "white"
    
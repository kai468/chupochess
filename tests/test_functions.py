
# run all tests via command line with command "python setup.py pytest" in home folder

def test_pieceColor_Not():
    from chupochess.common import PieceColor
    white = PieceColor.WHITE
    black = PieceColor(1)
    assert white != black
    assert white == black.Not()
    assert black == white.Not()
     
def test_LocationDictionary():
    from chupochess.common import Location, LocationDictionary, File
    dictionary = LocationDictionary()
    location = Location(1, File.A)
    dictionary[location] = "something"
    assert location in dictionary           # test in operator (__contains()__)
    assert dictionary[location]             # test getter (__getitem()__)
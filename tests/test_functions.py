
# run all tests via command line with command "python setup.py pytest" in home folder

from ast import While


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

def test_King_getCastlingRights():
    # TODO: write test for getCastlingRights 
    from chupochess.board import Board
    from chupochess.common import PieceColor, Location, File
    from itertools import filterfalse
    board = Board()
    # get king:
    kings = board.getPieceList(PieceColor.WHITE)
    kings[:] = filterfalse(lambda piece : (piece.name != "K"), board.getPieceList(PieceColor.WHITE))
    wKing = kings[0]
    assert wKing.name == "K"        
    assert len(wKing.getCastlingRights(board)) == 0
    # do some moves to allow kingside castling:
    # F1 -> F5
    fromSquare = board.locationSquareMap[Location(0, File.F)]
    fromSquare.currentPiece.makeMove(board.locationSquareMap[Location(4, File.F)])
    fromSquare.reset()
    assert len(wKing.getCastlingRights(board)) == 0
    # G1 -> G5
    fromSquare = board.locationSquareMap[Location(0, File.G)]
    fromSquare.currentPiece.makeMove(board.locationSquareMap[Location(4, File.G)])
    fromSquare.reset()
    assert len(wKing.getCastlingRights(board)) == 1
    # do some moves to allow queenside castling:
    # C1 -> C5
    fromSquare = board.locationSquareMap[Location(0, File.C)]
    fromSquare.currentPiece.makeMove(board.locationSquareMap[Location(4, File.C)])
    fromSquare.reset()
    assert len(wKing.getCastlingRights(board)) == 1
    # D1 -> D5
    fromSquare = board.locationSquareMap[Location(0, File.D)]
    fromSquare.currentPiece.makeMove(board.locationSquareMap[Location(4, File.D)])
    fromSquare.reset()
    assert len(wKing.getCastlingRights(board)) == 1
    # B1 -> B5
    fromSquare = board.locationSquareMap[Location(0, File.B)]
    fromSquare.currentPiece.makeMove(board.locationSquareMap[Location(4, File.B)])
    fromSquare.reset()
    assert len(wKing.getCastlingRights(board)) == 2
    # move kingside rook: H1->H5
    fromSquare = board.locationSquareMap[Location(0, File.H)]
    fromSquare.currentPiece.makeMove(board.locationSquareMap[Location(4, File.H)])
    fromSquare.reset()
    assert len(wKing.getCastlingRights(board)) == 1
    # move king: E1->D1
    fromSquare = board.locationSquareMap[Location(0, File.E)]
    fromSquare.currentPiece.makeMove(board.locationSquareMap[Location(0, File.D)])
    fromSquare.reset()
    assert len(wKing.getCastlingRights(board)) == 0


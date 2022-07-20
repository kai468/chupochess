from ast import Str
from enum import Enum

class PieceColor(Enum):
    WHITE = 0
    BLACK = 1

class Piece:
    def __init__(self, color: PieceColor) -> None:
        self.color = color
        self.currentSquare = None
        self.name = None        # TODO: why do I need a name? 
    
    def __str__(self) -> str:
        return "Piece{name=" + str(self.name) \
            + ",currentSquare=" + str(self.currentSquare) \
            + ",color=" + str(self.color.name) + "}"


class King(Piece):
    def __init__(self, color: PieceColor) -> None:
        Piece.__init__(self, color)
        self.name = "King"

class Queen(Piece):
    def __init__(self, color: PieceColor) -> None:
        Piece.__init__(self, color)
        self.name = "Queen"

class Bishop(Piece):
    def __init__(self, color: PieceColor) -> None:
        Piece.__init__(self, color)
        self.name = "Bishop"

class Knight(Piece):
    def __init__(self, color: PieceColor) -> None:
        Piece.__init__(self, color)
        self.name = "Knight"

class Rook(Piece):
    def __init__(self, color: PieceColor) -> None:
        Piece.__init__(self, color)
        self.name = "Rook"

class Pawn(Piece):
    def __init__(self, color: PieceColor) -> None:
        Piece.__init__(self, color)
        self.name = "Pawn"
from enum import Enum
import abc
from typing import List
from urllib.parse import _NetlocResultMixinStr

from chupochess.board import Board, Location, Square

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

# https://realpython.com/python-interface/#using-abstract-method-declaration
# https://realpython.com/python-interface/#java
# TODO: 
class MovableInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'getValidMoves') and 
                callable(subclass.getValidMoves) and 
                hasattr(subclass, 'makeMove') and 
                callable(subclass.makeMove) or 
                NotImplemented)

    @abc.abstractmethod
    def getValidMoves(self, board: Board) -> List[Location]:
        raise NotImplementedError

    @abc.abstractmethod
    def makeMove(self, square: Square) -> None:
        raise NotImplementedError


class King(Piece):
    def __init__(self, color: PieceColor) -> None:
        Piece.__init__(self, color)
        self.name = "King"

class Queen(Piece):
    def __init__(self, color: PieceColor) -> None:
        Piece.__init__(self, color)
        self.name = "Queen"

    def getValidMoves(self, board: Board) -> List[Location]:
        print(self.name + " -> getValidMoves()")
        return None

    
    def makeMove(self, square: Square) -> None:
        print(self.name + " -> makeMove()")
        return None

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

class Pawn(Piece,MovableInterface):
    def __init__(self, color: PieceColor) -> None:
        Piece.__init__(self, color)
        self.name = "Pawn"

    def getValidMoves(self, board: Board) -> List[Location]:
        print(self.name + " -> getValidMoves()")
        return None

    
    def makeMove(self, square: Square) -> None:
        print(self.name + " -> makeMove()")
        return None



import abc
from chupochess.board import Board
from chupochess.squares import Square
from chupochess.common import Location
from typing import List

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
    def makeMove(self, square: Square, board: Board) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def getDefendedLocations(self, board: Board) -> List[Location]:
        raise NotImplementedError
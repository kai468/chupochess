from chupochess.board import Board
from chupochess.pieces import Pawn, PieceColor, Piece, Queen

class Game:
    def __init__(self):
        self.data = "hallo"
        self.board = Board()

    def main(self) -> None:
        color = PieceColor.BLACK
        pawn = Pawn(color)
        self.printPiece(pawn)
        queen = Queen(PieceColor.WHITE)
        self.printPiece(queen)
        #print(self.board)

    def printPiece(self, piece: Piece):
        print(str(piece))

    
from chupochess.board import Board
from chupochess.common import File, Location
#from chupochess.pieces import Bishop, MovableInterface, Pawn, PieceColor, Queen, Rook

class Game:
    def __init__(self):
        pass
    def main(self) -> None:
        # TODO: inputs/gameplay
        board = Board()

        files = [file.name for file in File]

        while True:
            board.printBoard()
            #input format: A2->A3
            move = input()
            # TODO: refactor the following part:
            fromTo = move.split("->")
            fromFile = files.index(fromTo[0][0])
            fromRank = int(fromTo[0][1]) - 1
            toFile = files.index(fromTo[1][0])
            toRank = int(fromTo[1][1]) - 1
            # ######
            fromSquare = board.locationSquareMap[Location(file=File(fromFile), rank=fromRank)]
            toSquare = board.locationSquareMap[Location(file=File(toFile), rank=toRank)]

            fromSquare.currentPiece.makeMove(toSquare)
            fromSquare.reset()
            


    #def printPiece(self, piece: MovableInterface):
    #    piece.getValidMoves(self.board)

    
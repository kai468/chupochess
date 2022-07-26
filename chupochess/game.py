from select import select
from chupochess.board import Board
from chupochess.common import File, Location


class Game:
    def __init__(self):
        pass
    def main(self) -> None:
        # TODO: checkmate detection + draw detection
        # TODO: GUI
        board = Board()

        files = [file.name for file in File]

        validMoves = None

        while True:
            board.printBoard(validMoves=validMoves)
            #input format: A2->A3
            move = input()
            # TODO: refactor the following part:
            if move[0] == 's':
                # show possible moves
                # select piece
                selectedFile = files.index(move[1])
                selectedRank = int(move[2]) - 1
                selectedSquare = board.locationSquareMap[Location(file=File(selectedFile), rank=selectedRank)]
                # get valid moves
                validMoves = selectedSquare.currentPiece.getValidMoves(board)

            else:   # make move
                fromTo = move.split("->")
                fromFile = files.index(fromTo[0][0])
                fromRank = int(fromTo[0][1]) - 1
                toFile = files.index(fromTo[1][0])
                toRank = int(fromTo[1][1]) - 1
            # ######
                fromSquare = board.locationSquareMap[Location(file=File(fromFile), rank=fromRank)]
                toSquare = board.locationSquareMap[Location(file=File(toFile), rank=toRank)]
                
                fromSquare.currentPiece.makeMove(toSquare,board)
                
                validMoves = None



    #def printPiece(self, piece: MovableInterface):
    #    piece.getValidMoves(self.board)

    
from chupochess.common import Location, SquareColor, File, PieceColor, LocationDictionary
from chupochess.squares import Square

class Board:
    def __init__(self) -> None:
        from chupochess.pieces import PieceFactory
        self.boardSquares = []
        self.locationSquareMap = LocationDictionary()
        self.whitePieces = []
        self.blackPieces = []
        pieces = PieceFactory.getPieces()
        for file in range(8):
            currentFile = []
            for rank in range(8):
                currentColor = SquareColor(1) if ((file + rank)%2) == 0 else SquareColor(0)
                newSquare = Square(currentColor, Location(rank, File(file)))
                if newSquare.location in pieces:
                    piece = pieces[newSquare.location]
                    newSquare.isOccupied = True
                    newSquare.currentPiece = piece
                    piece.currentSquare = newSquare
                    if piece.color == PieceColor.BLACK:
                        self.blackPieces.append(piece)
                    else:
                        self.whitePieces.append(piece)
                self.locationSquareMap[newSquare.location] = newSquare
                currentFile.append(newSquare)
            self.boardSquares.append(currentFile)

    def __str__(self) -> str:
        # TODO: what would I use that function for? no information about pieces located on the board
        s = ""
        for file in range(8):
            for rank in range(8):
                s += str(self.boardSquares[file][rank])
            s+="\n"
        return s

    def printBoard(self) -> None:
        PREFIX_WHITE = '\033[93m'
        SUFFIX_WHITE = '\033[0m'
        print("  A B C D E F G H   ")
        sOut = ""
        for rank in range(7,-1,-1):
            sOut = str(rank + 1) + " "
            for file in range(8):
                if self.boardSquares[file][rank].isOccupied:
                    piece = self.boardSquares[file][rank].currentPiece
                    if piece.color == PieceColor.WHITE:
                        sOut += PREFIX_WHITE + piece.name[0] + SUFFIX_WHITE + " "
                    else:
                        sOut += piece.name[0] + " "
                else:
                    sOut += "_ "
            print(sOut + str(rank + 1))
        print("  A B C D E F G H   ")
            






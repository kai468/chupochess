from chupochess.common import Location, SquareColor, File, PieceColor, LocationDictionary
from chupochess.squares import Square
from typing import List

class Board:
    def __init__(self) -> None:
        from chupochess.pieces import PieceFactory
        self.boardSquares = []
        self.locationSquareMap = LocationDictionary()
        self.whitePieces = []
        self.blackPieces = []
        self.enPassantPossible = []
        self.whiteKingLocation = Location(0, File.E)
        self.blackKingLocation = Location(7, File.E)
        self.whiteToMove = True
        self.pins = []
        self.checks = []
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
                    piece.currentSquare = newSquare         # TODO: for bishop and rook lying "under" the queen/king, there is no square set (and therefore no location)
                    if piece.color == PieceColor.BLACK:
                        self.blackPieces.append(piece)
                    else:
                        self.whitePieces.append(piece)
                self.locationSquareMap[newSquare.location] = newSquare
                currentFile.append(newSquare)
            self.boardSquares.append(currentFile)

    def __str__(self) -> str:
        s = ""
        for file in range(8):
            for rank in range(8):
                s += str(self.boardSquares[file][rank])
            s+="\n"
        return s

    def printBoard(self, validMoves:List[Location]=None) -> None:
        ASCII_CLR_YELLOW = '\033[93m'
        ASCII_CLR_RED = '\033[91m'
        ASCII_CLR_RESET = '\033[0m'
        print("  A B C D E F G H   ")
        sOut = ""
        for rank in range(7,-1,-1):
            sOut = str(rank + 1) + " "
            for file in range(8):
                if self.boardSquares[file][rank].isOccupied:
                    piece = self.boardSquares[file][rank].currentPiece
                    if (validMoves is not None) and (Location(rank, File(file)) in validMoves):   
                        sOut += ASCII_CLR_RED + piece.name[0] + ASCII_CLR_RESET + " " # if isValidMove: mark red   
                    elif piece.color == PieceColor.WHITE:
                        sOut += ASCII_CLR_YELLOW + piece.name[0] + ASCII_CLR_RESET + " "
                    else:
                        sOut += piece.name[0] + " "
                elif (validMoves is not None) and (Location(rank, File(file)) in validMoves):
                    sOut += ASCII_CLR_RED + "_" + ASCII_CLR_RESET + " " 
                else:
                    sOut += "_ "
            print(sOut + str(rank + 1))
        print("  A B C D E F G H   ")

    def getPieceList(self, color: PieceColor) -> List[object]:
        if color == PieceColor.BLACK:
            return self.blackPieces.copy()
        else:
            return self.whitePieces.copy()

    def getKingLocation(self, color: PieceColor) -> Location:
        if color == PieceColor.BLACK:
            return self.blackKingLocation
        else:
            return self.whiteKingLocation

    def updatePieceList(self, piece: object) -> None:
        if not piece: return
        if piece.color == PieceColor.BLACK:
            self.blackPieces.remove(piece)
        elif piece.color == PieceColor.WHITE:
            self.whitePieces.remove(piece)

            







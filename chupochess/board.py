from chupochess.common import Location, SquareColor, File, PieceColor, LocationDictionary, GameState
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
        pieces = PieceFactory.getPieces()
        self.gameState = GameState.RUNNING
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
        s = ""
        for file in range(8):
            for rank in range(8):
                s += str(self.boardSquares[file][rank])
            s+="\n"
        return s

    def printBoard(self, validMoves:List[Location]=None) -> None:
        # debugging only
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
    
    def appendPieceList(self, piece: object):
        if piece.color == PieceColor.WHITE:
            self.whitePieces.append(piece)
        else:
            self.blackPieces.append(piece)

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

    def getSetup(self) -> dict:
        # only temporary, for HTML online GUI:
        setup = {}
        for piece in self.whitePieces:
            setup[str(piece.currentSquare.location)] = "w" + piece.name
        for piece in self.blackPieces:
            setup[str(piece.currentSquare.location)] = "b" + piece.name
        return setup

    def updateGameState(self) -> None:
        # TODO: performance point of view: probably it's best to first check if the king has any valid moves
        color = PieceColor.WHITE if self.whiteToMove else PieceColor.BLACK
        king = self.locationSquareMap[self.getKingLocation(color)].currentPiece
        kingMoves = king.getValidMoves(self)

        if self._isInsufficientMaterial(): 
            self.gameState = GameState.DRAW
        elif len(kingMoves) > 0:                                    # for performance reasons 
            return        
        elif len(king.isInCheck(self)) >= 2:                             # 2 opponent pieces attacking and no valid moves
            self.gameState = GameState(color.Not().value + 2)       # checkmate - opponent team wins
        else:
            # two relevant cases: 
            # a) one attacking piece, (no king moves), no other piece to block the attack -> checkmate
            # b) stalemate: not in check but no legal moves -> draw
            for piece in self.getPieceList(color):
                if len(piece.getValidMoves(self)) > 0: 
                    return                                          # for performance reasons 
            if len(king.isInCheck(self)) > 0:
                self.gameState = GameState(color.Not().value + 2)   # checkmate - opponent team wins
            else:
                self.gameState = GameState.DRAW                     # stalemate: not in check but no legal moves

        # TODO: missing for draw: threefold/fivefold repetition and fifty-move rule / seventy-five-move rule

    def _isInsufficientMaterial(self) -> bool:
        if len(self.whitePieces) > 2 or len(self.blackPieces) > 2:
            return False
        elif len(self.whitePieces) == 1 and len(self.blackPieces) == 1:
            return True
        else:
            # check for pieces other than king, bishop and knight:
            for piece in self.whitePieces:
                if piece.name not in ["K", "B", "N"]:
                    return False
            for piece in self.blackPieces: 
                if piece.name not in ["K", "B", "N"]:
                    return False
            return True
        


            







from itertools import filterfalse
from typing import List
from chupochess.board import Board
from chupochess.interfaces import MovableInterface
from chupochess.common import PieceColor, Location, LocationFactory, File, LocationDictionary
from chupochess.squares import Square

class Piece:
    def __init__(self, color: PieceColor) -> None:
        self.color = color
        self.currentSquare = None
        self.name = None        
    
    def __str__(self) -> str:
        return "Piece{name=" + str(self.name) \
            + ",currentSquare=" + str(self.currentSquare) \
            + ",color=" + str(self.color.name) + "}"


class King(Piece, MovableInterface):
    def __init__(self, color: PieceColor) -> None:
        Piece.__init__(self, color)
        self.name = "K"
        self.bishop = Bishop(color)
        self.rook = Rook(color)
        self.isFirstMove = True  
        self.castlingRights = []           

    def getValidMoves(self, board: Board, checkDetection: bool = True) -> List[Location]:
        moveCandidates = []
        moveCandidates.extend(self.bishop.getValidMoves(board, self.currentSquare))     
        moveCandidates.extend(self.rook.getValidMoves(board, self.currentSquare))      
        # filter if abs() > 1:
        moveCandidates[:] = filterfalse(lambda candidate : (abs(candidate.file.value - self.currentSquare.location.file.value) > 1) or (abs(candidate.rank - self.currentSquare.location.rank) > 1), moveCandidates)
        moveCandidates.extend(self.getCastlingRights(board))
        # "in check" detection for move candidates: 
        if checkDetection:
            locationsUnderAttack = []
            # TODO: there must be a more efficient way to do the following
            for opponentPiece in board.getPieceList(self.color.Not()):
                if opponentPiece.name == "K":
                    locationsUnderAttack.extend(opponentPiece.getValidMoves(board, False))
                else: 
                    locationsUnderAttack.extend(opponentPiece.getValidMoves(board))
            moveCandidates[:] = filterfalse(lambda candidate : candidate in locationsUnderAttack, moveCandidates)
        return moveCandidates

    def makeMove(self, square: Square, board: Board) -> None:
        # TODO: refactor makeMove (identical for all pieces but the Pawns)
        self.currentSquare.reset()
        self.currentSquare = square
        self.isFirstMove = False
        square.currentPiece = self
        square.isOccupied = True
        if self.color == PieceColor.WHITE:
            board.whiteKingLocation = self.currentSquare.location
        else:
            board.blackKingLocation = self.currentSquare.location
        # TODO: check if move is castling move. if yes: move rook, too. 

    def getCastlingRights(self, board: Board) -> List[Location]:
        castlingRights = []
        if self.isFirstMove:
            # get rooks that were not moved yet:
            rooks = board.getPieceList(self.color)
            rooks[:] = filterfalse(lambda piece : (piece.name != "R") or (piece.isFirstMove == False), rooks)
            for rook in rooks:
                if rook.currentSquare.location.file == File.A:
                    fileOffset = -3     # queenside / long castle
                else:
                    fileOffset = 2      # kingside / castle
                # check if any other pieces are blocking the path to castled position:
                pathBlocked = False
                cnt = -1 if fileOffset < 0 else 1 
                next = LocationFactory.build(self.currentSquare.location, cnt, 0)
                while(next in board.locationSquareMap):
                    if board.locationSquareMap[next].isOccupied:
                        pathBlocked = True
                        break
                    if cnt == fileOffset:
                        break
                    cnt = (cnt - 1) if fileOffset < 0 else (cnt + 1)
                    next = LocationFactory.build(self.currentSquare.location, cnt, 0)
                if pathBlocked == False:
                    castlingRights.append(LocationFactory.build(self.currentSquare.location, fileOffset, 0)) 
        self.castlingRights = castlingRights
        return castlingRights
        # TODO: check whether an opponent piece is attacking one of the squares on path to castled position
        #       (only the two squares on file C/D or F/G have to be checked, for long castle the B file is irrelevant)
    
    def isInCheck(self, board: Board) -> bool:
        # check whether King is under immediate attack:
        for opponentPiece in board.getPieceList(self.color.Not()):
            for location in opponentPiece.getValidMoves(board):
                if location == self.currentSquare.location:
                    return True
        return False

class Queen(Piece, MovableInterface):
    def __init__(self, color: PieceColor) -> None:
        Piece.__init__(self, color)
        self.name = "Q"
        self.bishop = Bishop(color)
        self.rook = Rook(color)

    def getValidMoves(self, board: Board) -> List[Location]:
        moveCandidates = []
        moveCandidates.extend(self.bishop.getValidMoves(board, self.currentSquare))  
        moveCandidates.extend(self.rook.getValidMoves(board, self.currentSquare))   
        return moveCandidates
    
    def makeMove(self, square: Square) -> None:
        self.currentSquare.reset()
        self.currentSquare = square
        square.currentPiece = self
        square.isOccupied = True

class Bishop(Piece, MovableInterface):
    def __init__(self, color: PieceColor) -> None:
        Piece.__init__(self, color)
        self.name = "B"

    def getValidMoves(self, board: Board, square: Square = None) -> List[Location]:
        if square == None: square = self.currentSquare
        squareMap = board.locationSquareMap
        offsets = [(-1,1), (1,1), (-1, -1), (1,-1)]
        moveCandidates = []
        for offset in offsets:
            # explore the field in every possible direction (rankwise and filewise)
            next = LocationFactory.build(square.location, offset[0], offset[1])
            while (next in squareMap):
                if squareMap[next].isOccupied:
                    if squareMap[next].currentPiece.color == self.color:
                        break
                    moveCandidates.append(next)
                    break
                moveCandidates.append(next)
                next = LocationFactory.build(next, offset[0], offset[1])
        return moveCandidates

    def makeMove(self, square: Square) -> None:
        self.currentSquare.reset()
        self.currentSquare = square
        square.currentPiece = self
        square.isOccupied = True

class Knight(Piece, MovableInterface):
    def __init__(self, color: PieceColor) -> None:
        Piece.__init__(self, color)
        self.name = "N"

    def getValidMoves(self, board: Board) -> List[Location]:
        moveCandidates = []
        squareMap = board.locationSquareMap
        offsets = [(-2,1),(-1,2),(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1)]
        for offset in offsets:
            next = LocationFactory.build(self.currentSquare.location, offset[0], offset[1])
            if next in squareMap:
                if squareMap[next].isOccupied == False:
                    moveCandidates.append(next)
                elif squareMap[next].currentPiece.color != self.color:
                    moveCandidates.append(next)
        return moveCandidates

    def makeMove(self, square: Square) -> None:
        self.currentSquare.reset()
        self.currentSquare = square
        square.currentPiece = self
        square.isOccupied = True

class Rook(Piece, MovableInterface):
    def __init__(self, color: PieceColor) -> None:
        Piece.__init__(self, color)
        self.name = "R"
        self.isFirstMove = True

    def getValidMoves(self, board: Board, square: Square = None) -> List[Location]:
        if square == None: square = self.currentSquare
        squareMap = board.locationSquareMap
        offsets = [(-1,0), (1,0), (0, -1), (0,1)]
        moveCandidates = []
        for offset in offsets:
            # explore the field in every possible direction (rankwise and filewise)
            next = LocationFactory.build(square.location, offset[0], offset[1])
            while (next in squareMap):
                if squareMap[next].isOccupied:
                    if squareMap[next].currentPiece.color == self.color:
                        break
                    moveCandidates.append(next)
                    break
                moveCandidates.append(next)
                next = LocationFactory.build(next, offset[0], offset[1])
        return moveCandidates

    def makeMove(self, square: Square) -> None:
        self.currentSquare.reset()
        self.currentSquare = square
        self.isFirstMove = False
        square.currentPiece = self
        square.isOccupied = True
        

class Pawn(Piece,MovableInterface):
    def __init__(self, color: PieceColor) -> None:
        Piece.__init__(self, color)
        self.name = "P"
        self.isFirstMove = True

    def getValidMoves(self, board: Board) -> List[Location]:
        currentLocation = self.currentSquare.location
        squareMap = board.locationSquareMap
        moveCandidates = []
        moveCandidates.append(LocationFactory.build(currentLocation, fileOffset=0, rankOffset=1))
        if self.isFirstMove:
            moveCandidates.append(LocationFactory.build(currentLocation, fileOffset=0, rankOffset=2))
        moveCandidates.append(LocationFactory.build(currentLocation, fileOffset=1, rankOffset=1))
        moveCandidates.append(LocationFactory.build(currentLocation, fileOffset=-1, rankOffset=1))
        # filter out locations that are not on the board:
        moveCandidates[:] = filterfalse(lambda candidate : candidate not in squareMap, moveCandidates)
        # move logic:
        # same-file moves (no capture) are only allowed if not blocked by other piece:
        moveCandidates[:] = filterfalse(lambda candidate : (candidate.file == currentLocation.file) and (squareMap[candidate].isOccupied == False), moveCandidates)
        # captures are only allowed if opponent's piece: 
        moveCandidates[:] = filterfalse(lambda candidate : (candidate.file != currentLocation.file) and (squareMap[candidate].isOccupied == True) and (squareMap[candidate].currentPiece.color != self.color), moveCandidates)
        # TODO: en passant captures + do not forward 2 squares if the first square is blocked
        return moveCandidates

    def makeMove(self, square: Square) -> None:
        if self.isFirstMove:
            self.isFirstMove = False
        self.currentSquare.reset()
        self.currentSquare = square
        square.currentPiece = self
        square.isOccupied = True


class PieceFactory:
    def __init__(self) -> None:
        pass
    def getPieces() -> dict:
        pieces = LocationDictionary()

        # pawns:
        for file in range(8):
            pieces[Location(1,File(file))] = Pawn(PieceColor.WHITE)
            pieces[Location(6,File(file))] = Pawn(PieceColor.BLACK)

        # rooks:
        pieces[Location(0, File.A)] = Rook(PieceColor.WHITE)
        pieces[Location(0, File.H)] = Rook(PieceColor.WHITE)
        pieces[Location(7, File.A)] = Rook(PieceColor.BLACK)
        pieces[Location(7, File.H)] = Rook(PieceColor.BLACK)

        # knights:
        pieces[Location(0, File.B)] = Knight(PieceColor.WHITE)
        pieces[Location(0, File.G)] = Knight(PieceColor.WHITE)
        pieces[Location(7, File.B)] = Knight(PieceColor.BLACK)
        pieces[Location(7, File.G)] = Knight(PieceColor.BLACK)

        # bishops:
        pieces[Location(0, File.C)] = Bishop(PieceColor.WHITE)
        pieces[Location(0, File.F)] = Bishop(PieceColor.WHITE)
        pieces[Location(7, File.C)] = Bishop(PieceColor.BLACK)
        pieces[Location(7, File.F)] = Bishop(PieceColor.BLACK)

        # queens:
        pieces[Location(0, File.D)] = Queen(PieceColor.WHITE)
        pieces[Location(7, File.D)] = Queen(PieceColor.BLACK)

        # kings:
        pieces[Location(0, File.E)] = King(PieceColor.WHITE)
        pieces[Location(7, File.E)] = King(PieceColor.BLACK)
        
        return pieces
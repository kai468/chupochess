from itertools import filterfalse
from typing import List, Tuple
from typing_extensions import Self
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

    def _switchSquaresAndCapture(self, targetSquare: Square, board: Board) -> None:
        self.currentSquare.reset()
        self.currentSquare = targetSquare
        board.updatePieceList(targetSquare.reset()) # make capture if there is sth to capture
        targetSquare.currentPiece = self
        targetSquare.isOccupied = True
        board.whiteToMove = not board.whiteToMove

    def isPinnedBy(self, board: Board, square: Square = None) -> Self:     # returns the "pinning" piece
        if square == None: square = self.currentSquare
        kingLocation = board.getKingLocation(self.color)
        squareMap = board.locationSquareMap
        # check if active piece is on a "attack path" relative to king:
        locationOffset = kingLocation.offset(square.location)
        if abs(locationOffset[0]) == abs(locationOffset[1]):
            # possible attackers: B/Q
            offset = (int(locationOffset[0]/abs(locationOffset[0])), int(locationOffset[1]/abs(locationOffset[1])))
            next = LocationFactory.build(kingLocation, offset[0], offset[1])
            relevantIndex = 0       # for bishops, absolute rank and file offsets should always be the same -> irrelevant
            attackers = ["B","Q"]
        elif (locationOffset[0] == 0 or locationOffset[1] == 0):
            # possible attackers: R/Q
            relevantIndex = 0 if locationOffset[1] == 0 else 1
            offset = (0 if relevantIndex == 1 else int(locationOffset[0]/abs(locationOffset[0])),
                      0 if relevantIndex == 0 else int(locationOffset[1]/abs(locationOffset[1])))
            next = LocationFactory.build(kingLocation, offset[0], offset[1])
            attackers = ["R", "Q"]
        else:
            return None
        while next in squareMap:
            if (squareMap[next].isOccupied == False) or (next == square.location):
                next = LocationFactory.build(next, offset[0], offset[1])
            elif abs(kingLocation.offset(next)[relevantIndex]) < abs(locationOffset[relevantIndex]): 
                # king is protected by other piece -> no pin!
                return None
            elif squareMap[next].currentPiece.color == self.color:
                # ally found -> no pin!
                return None
            elif (squareMap[next].currentPiece.color == self.color.Not()) and (squareMap[next].currentPiece.name not in attackers):
                # potential attacker is blocked by other opponent piece -> no pin!
                return None
            else: 
                # attacker found:
                return squareMap[next].currentPiece


class King(Piece, MovableInterface):
    def __init__(self, color: PieceColor) -> None:
        Piece.__init__(self, color)
        self.name = "K"
        self.bishop = Bishop(color)
        self.rook = Rook(color)
        self.isFirstMove = True  
        self.castlingRights = []           

    def getValidMoves(self, board: Board) -> List[Location]:
        moveCandidates = []
        moveCandidates.extend(self.bishop.getValidMoves(board, self.currentSquare))     
        moveCandidates.extend(self.rook.getValidMoves(board, self.currentSquare))      
        # filter if abs() > 1:
        moveCandidates[:] = filterfalse(lambda candidate : (abs(candidate.file.value - self.currentSquare.location.file.value) > 1) or (abs(candidate.rank - self.currentSquare.location.rank) > 1), moveCandidates)
        moveCandidates.extend(self.getCastlingRights(board))
        # "in check" detection for move candidates: 
        #if checkDetection:
        locationsUnderAttack = []
        # TODO: there must be a more efficient way to do the following
        for opponentPiece in board.getPieceList(self.color.Not()):
            locationsUnderAttack.extend(opponentPiece.getDefendedLocations(board))
        moveCandidates[:] = filterfalse(lambda candidate : candidate in locationsUnderAttack, moveCandidates)
        return moveCandidates

    def getDefendedLocations(self, board: Board) -> List[Location]:
        defendedLocations = []
        defendedLocations.extend(self.bishop.getDefendedLocations(board, self.currentSquare))
        defendedLocations.extend(self.rook.getDefendedLocations(board, self.currentSquare))
        defendedLocations[:] = filterfalse(lambda candidate : (abs(candidate.file.value - self.currentSquare.location.file.value) > 1) or (abs(candidate.rank - self.currentSquare.location.rank) > 1), defendedLocations)
        return defendedLocations

    def makeMove(self, square: Square, board: Board) -> None:
        if abs(self.currentSquare.location.file.value - square.location.file.value) > 1:
            # castling move -> move rook, too:
            rooks = board.getPieceList(self.color)
            if square.location.file == File.G:
                # short castle -> rook has to be moved from file H to F
                rooks[:] = filterfalse(lambda piece : (piece.name != "R") or (piece.currentSquare.location != Location(self.currentSquare.location.rank, File.H)), rooks)
                rooks[0].makeMove(board.locationSquareMap[Location(self.currentSquare.location.rank, File.F)], board)
            else:
                # long castle -> rook has to be moved from file A to D
                rooks[:] = filterfalse(lambda piece : (piece.name != "R") or (piece.currentSquare.location != Location(self.currentSquare.location.rank, File.A)), rooks)
                rooks[0].makeMove(board.locationSquareMap[Location(self.currentSquare.location.rank, File.D)], board)
        self.isFirstMove = False
        self._switchSquaresAndCapture(square, board)

        if self.color == PieceColor.WHITE:
            board.whiteKingLocation = self.currentSquare.location
        else:
            board.blackKingLocation = self.currentSquare.location
        board.enPassantPossible.clear()

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
                    elif abs(cnt <= 2) and self._castlingSquareUnderAttack(cnt, board):
                        # check if squares on File C/D or F/G are under attack
                        pathBlocked = True
                        break
                    if cnt == fileOffset:
                        break
                    cnt = (cnt - 1) if fileOffset < 0 else (cnt + 1)
                    next = LocationFactory.build(self.currentSquare.location, cnt, 0)
                if pathBlocked == False:
                    if fileOffset == -3:
                        fileOffset = -2     # king's target position is relevant for the Location
                    castlingRights.append(LocationFactory.build(self.currentSquare.location, fileOffset, 0)) 
        # no castling if king is in check:
        if self.isInCheck(board):
            castlingRights.clear()
        self.castlingRights = castlingRights
        return castlingRights

    def _castlingSquareUnderAttack(self, fileOffset: int, board: Board) -> bool:
        squareMap = board.locationSquareMap
        # TODO: refactor: locations in 2nd/7th file are build multiple times (checked for king, then for pawns, then for bishop/rook/queen)
        
        # potential attacker: opponents king
        offsets = [(-1,1),(0,1),(1,1)] if self.color == PieceColor.WHITE else [(-1,-1),(0,-1),(1,-1)]
        for offset in offsets:
            attackerLocation = LocationFactory.build(self.currentSquare.location, fileOffset + offset[0], offset[1])
            if attackerLocation in squareMap and squareMap[attackerLocation].isOccupied and squareMap[attackerLocation].currentPiece.name == "P" and squareMap[attackerLocation].currentPiece.color != self.color:
                return True

        # potential attacker: pawn 
        offsets = [(-1,1),(1,1)] if self.color == PieceColor.WHITE else [(-1,-1),(1,-1)]
        for offset in offsets:
            attackerLocation = LocationFactory.build(self.currentSquare.location, fileOffset + offset[0], offset[1])
            if attackerLocation in squareMap and squareMap[attackerLocation].isOccupied and squareMap[attackerLocation].currentPiece.name == "P" and squareMap[attackerLocation].currentPiece.color != self.color:
                return True

        # potential attacker: knight -> offset: List[Tupel[file: int, rank: int]]
        offsets = [(-2,1),(-1,2),(1,2),(2,1)] if self.color == PieceColor.WHITE else [(2,-1),(1,-2),(-1,-2),(-2,-1)]    
        for offset in offsets:
            attackerLocation = LocationFactory.build(self.currentSquare.location, fileOffset + offset[0], offset[1])
            if attackerLocation in squareMap and squareMap[attackerLocation].isOccupied and squareMap[attackerLocation].currentPiece.name == "N" and squareMap[attackerLocation].currentPiece.color != self.color:
                return True

        # potential attacker: rook/queen/bishop -> offset: List[Tupel[file: int, rank: int, relevantAttackers: List[str]]]
        if self.color == PieceColor.WHITE:
            offsets = [(-1,1,["B","Q"]),(1,1,["B","Q"]),(0,1,["R","Q"]),(int(fileOffset / abs(fileOffset)),0,["R","Q"])]
        else:
            offsets = [(-1,-1,["B","Q"]),(1,-1,["B","Q"]),(0,-1,["R","Q"]),(int(fileOffset / abs(fileOffset)),0,["R","Q"])]
        for offset in offsets:
            attackerLocation = LocationFactory.build(self.currentSquare.location, fileOffset + offset[0], offset[1])
            while attackerLocation in squareMap:
                if squareMap[attackerLocation].isOccupied:
                    if squareMap[attackerLocation].currentPiece.color != self.color and (squareMap[attackerLocation].currentPiece.name in offset[2]):
                        return True
                    else:
                        break
                attackerLocation = LocationFactory.build(attackerLocation, offset[0], offset[1])
        
        return False
        
    
    def isInCheck(self, board: Board) -> bool:
        # TODO: it would probably be more efficient to use the same algorithm as in _castlingSquareUnderAttack
        # check whether King is under immediate attack:
        for opponentPiece in (piece for piece in board.getPieceList(self.color.Not()) if piece.name != "K"):
            for location in (loc for loc in opponentPiece.getValidMoves(board) if loc == self.currentSquare.location):
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

    def getDefendedLocations(self, board: Board) -> List[Location]:
        defendedLocations = []
        defendedLocations.extend(self.bishop.getDefendedLocations(board, self.currentSquare))
        defendedLocations.extend(self.rook.getDefendedLocations(board, self.currentSquare))
        return defendedLocations
    
    def makeMove(self, square: Square, board: Board) -> None:
        self._switchSquaresAndCapture(square, board)
        board.enPassantPossible.clear()

class Bishop(Piece, MovableInterface):
    def __init__(self, color: PieceColor) -> None:
        Piece.__init__(self, color)
        self.name = "B"

    def getValidMoves(self, board: Board, square: Square = None, includeDefendedLocations: bool = False) -> List[Location]:
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
                        if includeDefendedLocations:
                            moveCandidates.append(next)
                        break
                    moveCandidates.append(next)
                    break
                moveCandidates.append(next)
                next = LocationFactory.build(next, offset[0], offset[1])
        # check if piece is pinned:
        attacker = self.isPinnedBy(board, square)
        if attacker:
            attackerOffset = square.location.offset(attacker.currentSquare.location)
            if 0 in attackerOffset:
                # attacker on the same rank or file -> no movement possible
                moveCandidates.clear()
            else:
                # attacker on the same diagonal -> limited movement possible
                # (only in direction of offset or in inverse direction)
                moveCandidates[:] = filterfalse(lambda candidate : (int(candidate.offset(square.location)[0]/abs(candidate.offset(square.location)[0])),candidate.offset(square.location)[1]/abs(candidate.offset(square.location)[1])) not in self._limitMovementPinnedBishop(attackerOffset), moveCandidates)
                # TODO: this became horribly unreadable -> refactor!
        return moveCandidates

    def _limitMovementPinnedBishop(self, attackerOffset: Tuple[int,int]) -> Tuple[Tuple[int,int], Tuple[int,int]]:
        norm = (int(attackerOffset[0]/abs(attackerOffset[0])),int(attackerOffset[1]/abs(attackerOffset[1])))
        inv = (-norm[0], -norm[1])
        return (norm, inv)
                
    def getDefendedLocations(self, board: Board, square: Square = None) -> List[Location]:
        return self.getValidMoves(board, square, True)

    def makeMove(self, square: Square, board: Board) -> None:
        self._switchSquaresAndCapture(square, board)
        board.enPassantPossible.clear()

class Knight(Piece, MovableInterface):
    def __init__(self, color: PieceColor) -> None:
        Piece.__init__(self, color)
        self.name = "N"

    def getValidMoves(self, board: Board, includeDefendedLocations: bool = False) -> List[Location]:
        moveCandidates = []
        squareMap = board.locationSquareMap
        offsets = [(-2,1),(-1,2),(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1)]
        if self.isPinnedBy(board):
            # knight is pinned -> no movement possible
            return moveCandidates
        for offset in offsets:
            next = LocationFactory.build(self.currentSquare.location, offset[0], offset[1])
            if next in squareMap:
                if squareMap[next].isOccupied == False:
                    moveCandidates.append(next)
                elif squareMap[next].currentPiece.color != self.color:
                    moveCandidates.append(next)
                elif includeDefendedLocations:
                    moveCandidates.append(next)
        return moveCandidates

    def getDefendedLocations(self, board: Board) -> List[Location]:
        return self.getValidMoves(board, True)

    def makeMove(self, square: Square, board: Board) -> None:
        self._switchSquaresAndCapture(square, board)
        board.enPassantPossible.clear()

class Rook(Piece, MovableInterface):
    def __init__(self, color: PieceColor) -> None:
        Piece.__init__(self, color)
        self.name = "R"
        self.isFirstMove = True

    def getValidMoves(self, board: Board, square: Square = None, includeDefendedLocations: bool = False) -> List[Location]:
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
                        if includeDefendedLocations:
                            moveCandidates.append(next)
                        break
                    moveCandidates.append(next)
                    break
                moveCandidates.append(next)
                next = LocationFactory.build(next, offset[0], offset[1])
        # check if piece is pinned:
        attacker = self.isPinnedBy(board, square)
        if attacker:
            attackerOffset = square.location.offset(attacker.currentSquare.location)
            if 0 in attackerOffset: 
                # attacker on same rank or file -> limited movement possible
                # (only in direction of offset or in inverse direction)
                noMovementIndex = 0 if attackerOffset[0] == 0 else 1
                moveCandidates[:] = filterfalse(lambda candidate : candidate.offset(square.location)[noMovementIndex] != 0, moveCandidates)
                # TODO: this became horribly unreadable -> refactor!
            else:
                # attacker attacking diagonally -> no movement possible
                moveCandidates.clear()
        return moveCandidates

    def getDefendedLocations(self, board: Board, square: Square = None) -> List[Location]:
        return self.getValidMoves(board, square, True)

    def makeMove(self, square: Square, board: Board) -> None:
        self.isFirstMove = False
        self._switchSquaresAndCapture(square, board)
        board.enPassantPossible.clear()
        

class Pawn(Piece,MovableInterface):
    def __init__(self, color: PieceColor) -> None:
        Piece.__init__(self, color)
        self.name = "P"
        self.isFirstMove = True
        self.enPassantPossible = False

    def getValidMoves(self, board: Board) -> List[Location]:
        rankOffset = 1 if self.color == PieceColor.WHITE else -1
        currentLocation = self.currentSquare.location
        squareMap = board.locationSquareMap
        moveCandidates = []
        moveCandidates.append(LocationFactory.build(currentLocation, 0, rankOffset))
        if self.isFirstMove and (squareMap[moveCandidates[0]].isOccupied == False):
            moveCandidates.append(LocationFactory.build(currentLocation, 0, 2*rankOffset))
        moveCandidates.append(LocationFactory.build(currentLocation, 1, rankOffset))
        moveCandidates.append(LocationFactory.build(currentLocation, -1, rankOffset))
        # move Logic:
        # a) filter out locations that are not on the board
        # b) same-file moves (no capture) are not allowed if blocked by other piece
        # c) file-crossing moves are not allowed if there is no piece to capture
        # d) captures are only allowed if it's an opponent's piece
        moveCandidates[:] = filterfalse(lambda candidate: \
            True if (candidate not in squareMap) else (
                True if ((candidate.file == currentLocation.file) and squareMap[candidate].isOccupied) else (
                    True if ((candidate.file != currentLocation.file) and (squareMap[candidate].isOccupied == False)) else (
                        True if ((candidate.file != currentLocation.file) and (squareMap[candidate].isOccupied == True) and (squareMap[candidate].currentPiece.color == self.color)) else False
                    )
                )
            ), moveCandidates)

        # en passant captures:
        for enPassant in board.enPassantPossible:
            if (enPassant.color != self.color) and (enPassant.currentSquare.location in [LocationFactory.build(currentLocation, -1, 0), LocationFactory.build(currentLocation, 1, 0)]):
                moveCandidates.append(LocationFactory.build(enPassant.currentSquare.location, 0, rankOffset))
        # check if pawn is pinned:
        attacker = self.isPinnedBy(board)
        if attacker:
            attackerOffset = currentLocation.offset(attacker.currentSquare.location)
            if attackerOffset[1] == 0 :
                # attacker on same rank -> no movement possible
                moveCandidates.clear()
            elif attackerOffset[0] == 0:
                # attacker on same file -> limited movement possible
                pass # filterfalse -> everything with a file offset
                moveCandidates[:] = filterfalse(lambda candidate : candidate.offset(currentLocation)[0] != 0, moveCandidates)
            else:
                # attacker on the same diagonal -> limited movement possible (only captures in the right direction)
                 moveCandidates[:] = filterfalse(lambda candidate : (candidate.offset(currentLocation)[0],candidate.offset(currentLocation)[1]) not in self._limitMovementPinnedPawn(attackerOffset), moveCandidates)
        return moveCandidates

    def _limitMovementPinnedPawn(self, attackerOffset: Tuple[int,int]) -> Tuple[Tuple[int,int], Tuple[int,int]]:
        norm = (int(attackerOffset[0]/abs(attackerOffset[0])),int(attackerOffset[1]/abs(attackerOffset[1])))
        inv = (-norm[0], -norm[1])
        return (norm, inv)

    def getDefendedLocations(self, board: Board) -> List[Location]:
        currentLocation = self.currentSquare.location
        defendedLocations = []
        rankOffset = 1 if self.color == PieceColor.WHITE else -1
        defendedLocations.append(LocationFactory.build(currentLocation, 1, rankOffset))
        defendedLocations.append(LocationFactory.build(currentLocation, -1, rankOffset))
        defendedLocations[:] = filterfalse(lambda candidate : candidate not in board.locationSquareMap, defendedLocations)
        return defendedLocations

    def makeMove(self, square: Square, board: Board) -> None:
        if self.isFirstMove:
            self.isFirstMove = False
            if abs(self.currentSquare.location.rank - square.location.rank) > 1:
                self.enPassantPossible = True
                board.enPassantPossible.clear()
                board.enPassantPossible.append(self)        
        # capture other pawn if en passant move:
        if (len(board.enPassantPossible) > 0) and (square.location.file != self.currentSquare.location.file):
            for enPassant in board.enPassantPossible:
                if (enPassant.color != self.color) and (enPassant.currentSquare.location.file == square.location.file):
                    board.updatePieceList(enPassant.currentSquare.reset())
                    board.enPassantPossible.clear()
                    break
        if self._isPawnPromotionMove(square, board):
            self._promotePawn(square, board)
        else:
            self._switchSquaresAndCapture(square, board)
        if not self in board.enPassantPossible:
            board.enPassantPossible.clear()

    def _isPawnPromotionMove(self, targetSquare: Square, board: Board) -> bool:
        if self.color == PieceColor.WHITE:
            return (targetSquare.location.rank == 7)
        else:
            return (targetSquare.location.rank == 0)

    def _promotePawn(self, targetSquare: Square, board: Board, cls: Piece = Queen):
        # TODO: interface for really choosing the cls -> e.g. promoting to a Knight, too
        board.updatePieceList(self.currentSquare.reset())
        promotedPiece = cls(self.color)
        promotedPiece.currentSquare = targetSquare
        targetSquare.currentPiece = promotedPiece
        targetSquare.isOccupied = True
        board.whiteToMove = not board.whiteToMove
        board.whitePieces.append(promotedPiece)
        


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
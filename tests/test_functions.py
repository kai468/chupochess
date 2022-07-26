# run all tests via command line with command "python setup.py pytest" in home folder

def test_pieceColor_Not():
    from chupochess.common import PieceColor
    white = PieceColor.WHITE
    black = PieceColor(1)
    assert white != black
    assert white == black.Not()
    assert black == white.Not()
     
def test_LocationDictionary():
    from chupochess.common import Location, LocationDictionary, File
    dictionary = LocationDictionary()
    location = Location(1, File.A)
    assert location not in dictionary
    dictionary[location] = "something"
    assert location in dictionary                           # test in operator (__contains()__)
    assert dictionary[location] == "something"              # test getter (__getitem()__)

def test_Location_offset():
    from chupochess.common import Location, File
    location1 = Location(0, File.A)
    location2 = Location(7, File.H)
    location3 = Location(0, File.B)
    assert location1.offset(location2) == (7,7)
    assert location2.offset(location3) == (-6,-7)

def test_Pawn_promotion():
    from chupochess.board import Board
    from chupochess.common import Location, File
    board = Board()
    files = [file.name for file in File]
    def makeMove(sFrom: str, sTo: str) -> None:
        # input format: sFrom/sTo = "A8"
        fromSquare = board.locationSquareMap[Location(int(sFrom[1]) - 1, File(files.index(sFrom[0])))]
        toSquare = board.locationSquareMap[Location(int(sTo[1]) - 1, File(files.index(sTo[0])))]
        fromSquare.currentPiece.makeMove(toSquare, board)
    def cntPieces(lst: object, name: str) -> int:
        cnt = 0
        for o in lst:
            if o.name == name:
                cnt+=1
        return cnt
    makeMove("G8", "F6")
    makeMove("G7", "H6")
    makeMove("G2", "G7")
    assert len(board.blackPieces) == 16
    assert len(board.whitePieces) == 16
    assert cntPieces(board.whitePieces, "P") == 8
    assert cntPieces(board.blackPieces, "P") == 8
    assert cntPieces(board.whitePieces, "Q") == 1
    assert cntPieces(board.blackPieces, "Q") == 1
    makeMove("G7","G8")
    assert len(board.blackPieces) == 16
    assert len(board.whitePieces) == 16
    assert cntPieces(board.whitePieces, "P") == 7
    assert cntPieces(board.blackPieces, "P") == 8
    assert cntPieces(board.whitePieces, "Q") == 2
    assert cntPieces(board.blackPieces, "Q") == 1

def test_Pawn_dontCaptureAlly():
    from chupochess.board import Board
    from chupochess.common import Location, File
    board = Board()
    files = [file.name for file in File]
    def makeMove(sFrom: str, sTo: str) -> None:
        # input format: sFrom/sTo = "A8"
        fromSquare = board.locationSquareMap[Location(int(sFrom[1]) - 1, File(files.index(sFrom[0])))]
        toSquare = board.locationSquareMap[Location(int(sTo[1]) - 1, File(files.index(sTo[0])))]
        fromSquare.currentPiece.makeMove(toSquare, board)
    pawn = board.locationSquareMap[Location(1, File.D)].currentPiece
    assert len(pawn.getValidMoves(board)) == 2
    makeMove("D2","D3")
    assert len(pawn.getValidMoves(board)) == 1
    makeMove("C2","C4")
    assert len(pawn.getValidMoves(board)) == 1
    makeMove("C7", "C4")
    assert len(pawn.getValidMoves(board)) == 2



def test_Piece_isPinnedBy_Bishop():
    from chupochess.board import Board
    from chupochess.common import Location, File
    board = Board()
    files = [file.name for file in File]
    def makeMove(sFrom: str, sTo: str) -> None:
        # input format: sFrom/sTo = "A8"
        fromSquare = board.locationSquareMap[Location(int(sFrom[1]) - 1, File(files.index(sFrom[0])))]
        toSquare = board.locationSquareMap[Location(int(sTo[1]) - 1, File(files.index(sTo[0])))]
        fromSquare.currentPiece.makeMove(toSquare, board)
    makeMove("E1", "E4")
    makeMove("D2", "D5")
    pawn = board.locationSquareMap[Location(4, File.D)].currentPiece
    assert pawn.isPinnedBy(board) == None
    makeMove("C8", "B7")
    assert pawn.isPinnedBy(board).name == "B"

def test_Rook_isPinnedBy_Rook():
    from chupochess.board import Board
    from chupochess.common import Location, File
    board = Board()
    files = [file.name for file in File]
    def makeMove(sFrom: str, sTo: str) -> None:
        # input format: sFrom/sTo = "A8"
        fromSquare = board.locationSquareMap[Location(int(sFrom[1]) - 1, File(files.index(sFrom[0])))]
        toSquare = board.locationSquareMap[Location(int(sTo[1]) - 1, File(files.index(sTo[0])))]
        fromSquare.currentPiece.makeMove(toSquare, board)
    makeMove("E8", "B6")
    makeMove("H8", "F6")
    rook = board.locationSquareMap[Location(5, File.F)].currentPiece
    assert rook.isPinnedBy(board) == None
    assert len(rook.getValidMoves(board)) > 5
    makeMove("D1", "H6")
    assert rook.isPinnedBy(board).name == "Q"
    assert len(rook.getValidMoves(board)) == 5

def test_Queen_isPinnedBy_Bishop():
    from chupochess.board import Board
    from chupochess.common import Location, File
    board = Board()
    files = [file.name for file in File]
    def makeMove(sFrom: str, sTo: str) -> None:
        # input format: sFrom/sTo = "A8"
        fromSquare = board.locationSquareMap[Location(int(sFrom[1]) - 1, File(files.index(sFrom[0])))]
        toSquare = board.locationSquareMap[Location(int(sTo[1]) - 1, File(files.index(sTo[0])))]
        fromSquare.currentPiece.makeMove(toSquare, board)
    makeMove("D1","D2")
    queen = board.locationSquareMap[Location(1, File.D)].currentPiece
    assert queen.isPinnedBy(board) == None
    assert len(queen.getValidMoves(board)) > 5
    makeMove("F8","C3")
    assert queen.isPinnedBy(board).name == "B"
    assert len(queen.getValidMoves(board)) == 1

def test_Piece_isPinnedBy_Rook():
    from chupochess.board import Board
    from chupochess.common import Location, File
    board = Board()
    files = [file.name for file in File]
    def makeMove(sFrom: str, sTo: str) -> None:
        # input format: sFrom/sTo = "A8"
        fromSquare = board.locationSquareMap[Location(int(sFrom[1]) - 1, File(files.index(sFrom[0])))]
        toSquare = board.locationSquareMap[Location(int(sTo[1]) - 1, File(files.index(sTo[0])))]
        fromSquare.currentPiece.makeMove(toSquare, board)
    makeMove("E8", "E6")
    makeMove("G8", "F6")
    knight = board.locationSquareMap[Location(5, File.F)].currentPiece
    assert knight.isPinnedBy(board) == None
    assert len(knight.getValidMoves(board)) > 0
    makeMove("A1", "H6")
    assert knight.isPinnedBy(board).name == "R"
    assert len(knight.getValidMoves(board)) == 0
    makeMove("G7","G6")
    assert knight.isPinnedBy(board) == None
    assert len(knight.getValidMoves(board)) > 0

def test_Pawn_isPinnedBy_Rook_File():
    from chupochess.board import Board
    from chupochess.common import Location, File
    board = Board()
    files = [file.name for file in File]
    def makeMove(sFrom: str, sTo: str) -> None:
        # input format: sFrom/sTo = "A8"
        fromSquare = board.locationSquareMap[Location(int(sFrom[1]) - 1, File(files.index(sFrom[0])))]
        toSquare = board.locationSquareMap[Location(int(sTo[1]) - 1, File(files.index(sTo[0])))]
        fromSquare.currentPiece.makeMove(toSquare, board)
    makeMove("E2", "E3")
    makeMove("D7", "D4")
    makeMove("F7", "F4")
    pawn = board.locationSquareMap[Location(2, File.E)].currentPiece
    assert pawn.isPinnedBy(board) == None
    assert len(pawn.getValidMoves(board)) == 3
    makeMove("H8","E6")
    assert pawn.isPinnedBy(board).name == "R"
    assert len(pawn.getValidMoves(board)) == 1
    makeMove("E6","E4")
    assert pawn.isPinnedBy(board).name == "R"
    assert len(pawn.getValidMoves(board)) == 0

def test_Pawn_isPinnedBy_Rook_Rank():
    from chupochess.board import Board
    from chupochess.common import Location, File
    board = Board()
    files = [file.name for file in File]
    def makeMove(sFrom: str, sTo: str) -> None:
        # input format: sFrom/sTo = "A8"
        fromSquare = board.locationSquareMap[Location(int(sFrom[1]) - 1, File(files.index(sFrom[0])))]
        toSquare = board.locationSquareMap[Location(int(sTo[1]) - 1, File(files.index(sTo[0])))]
        fromSquare.currentPiece.makeMove(toSquare, board)
    makeMove("E8", "C5")
    makeMove("E7", "E5")
    pawn = board.locationSquareMap[Location(4, File.E)].currentPiece
    assert pawn.isPinnedBy(board) == None
    assert len(pawn.getValidMoves(board)) == 1
    makeMove("D1", "G5")
    assert pawn.isPinnedBy(board).name == "Q"
    assert len(pawn.getValidMoves(board)) == 0

def test_Pawn_isPinnedBy_Bishop():
    from chupochess.board import Board
    from chupochess.common import Location, File
    board = Board()
    files = [file.name for file in File]
    def makeMove(sFrom: str, sTo: str) -> None:
        # input format: sFrom/sTo = "A8"
        fromSquare = board.locationSquareMap[Location(int(sFrom[1]) - 1, File(files.index(sFrom[0])))]
        toSquare = board.locationSquareMap[Location(int(sTo[1]) - 1, File(files.index(sTo[0])))]
        fromSquare.currentPiece.makeMove(toSquare, board)
    pawn = board.locationSquareMap[Location(6, File.D)].currentPiece
    assert pawn.isPinnedBy(board) == None
    makeMove("F1", "B5")
    assert pawn.isPinnedBy(board).name == "B"
    assert len(pawn.getValidMoves(board)) == 0
    makeMove("C1", "E6")
    assert pawn.isPinnedBy(board).name == "B"
    assert len(pawn.getValidMoves(board)) == 0
    makeMove("B5", "C6")
    assert pawn.isPinnedBy(board).name == "B"
    assert len(pawn.getValidMoves(board)) == 1
    
def test_King_inCheckDetection():
    from chupochess.board import Board
    from chupochess.common import PieceColor, Location, File
    from itertools import filterfalse
    board = Board()
    files = [file.name for file in File]
    def makeMove(sFrom: str, sTo: str) -> None:
        # input format: sFrom/sTo = "A8"
        fromSquare = board.locationSquareMap[Location(int(sFrom[1]) - 1, File(files.index(sFrom[0])))]
        toSquare = board.locationSquareMap[Location(int(sTo[1]) - 1, File(files.index(sTo[0])))]
        fromSquare.currentPiece.makeMove(toSquare, board)
    
    # get king:
    kings = board.getPieceList(PieceColor.BLACK)
    kings[:] = filterfalse(lambda piece : (piece.name != "K"), board.getPieceList(PieceColor.BLACK))
    bKing = kings[0]
    assert bKing.name == "K"        
    assert len(bKing.isInCheck(board)) == 0
    # attack King with Knight from G1:
    makeMove("G1","F6")
    assert len(bKing.isInCheck(board)) == 1
    makeMove("F6","G1")
    makeMove("E7","E3")
    assert len(bKing.isInCheck(board)) == 0
    makeMove("D1", "E3")
    assert len(bKing.isInCheck(board)) == 1

def test_board_whiteToMove():
    from chupochess.board import Board
    from chupochess.common import Location, File
    board = Board()
    files = [file.name for file in File]
    def makeMove(sFrom: str, sTo: str) -> None:
        # input format: sFrom/sTo = "A8"
        fromSquare = board.locationSquareMap[Location(int(sFrom[1]) - 1, File(files.index(sFrom[0])))]
        toSquare = board.locationSquareMap[Location(int(sTo[1]) - 1, File(files.index(sTo[0])))]
        fromSquare.currentPiece.makeMove(toSquare, board)

    assert board.whiteToMove == True
    makeMove("E2", "E4")
    assert board.whiteToMove == False
    makeMove("E7", "E5")
    assert board.whiteToMove == True

def test_King_getCastlingRights():
    from chupochess.board import Board
    from chupochess.common import PieceColor, Location, File
    from itertools import filterfalse
    board = Board()
    files = [file.name for file in File]
    def makeMove(sFrom: str, sTo: str) -> None:
        # input format: sFrom/sTo = "A8"
        fromSquare = board.locationSquareMap[Location(int(sFrom[1]) - 1, File(files.index(sFrom[0])))]
        toSquare = board.locationSquareMap[Location(int(sTo[1]) - 1, File(files.index(sTo[0])))]
        fromSquare.currentPiece.makeMove(toSquare, board)
    
    # get king:
    kings = board.getPieceList(PieceColor.WHITE)
    kings[:] = filterfalse(lambda piece : (piece.name != "K"), board.getPieceList(PieceColor.WHITE))
    wKing = kings[0]
    assert wKing.name == "K"        
    assert len(wKing.getCastlingRights(board)) == 0
    # do some moves to allow kingside castling:
    makeMove("F1", "F5")
    assert len(wKing.getCastlingRights(board)) == 0
    makeMove("G1", "G5")
    assert len(wKing.getCastlingRights(board)) == 1
    # do some moves to allow queenside castling:
    makeMove("C1", "C5")
    assert len(wKing.getCastlingRights(board)) == 1
    makeMove("D1", "D5")
    assert len(wKing.getCastlingRights(board)) == 1
    makeMove("B1", "B5")
    assert len(wKing.getCastlingRights(board)) == 2
    # check if attacked squares are identified correctly:
    # H8 -> C5 and C2 -> D3 to attack C1 with the rook on C5
    makeMove("H8", "C5")
    makeMove("C2", "D3")
    assert len(wKing.getCastlingRights(board)) == 1
    # H2 -> G3 and D8 -> H2 to attack F1 with the queen on H2
    makeMove("H2", "G3")
    makeMove("D8", "H2")
    assert len(wKing.getCastlingRights(board)) == 0
    # D3 -> C2 and H2 -> G3 to block/remove attackers:
    makeMove("D3", "C2")
    makeMove("H2", "G3")
    assert len(wKing.getCastlingRights(board)) == 2
    # castling not possible if king is in check:
    makeMove("F2","F3")
    assert len(wKing.getCastlingRights(board)) == 0
    # remove check:
    makeMove("G3", "D8")
    assert len(wKing.getCastlingRights(board)) == 2
    # move kingside rook: H1->H5
    makeMove("H1", "H5")
    assert len(wKing.getCastlingRights(board)) == 1
    # move king: E1->D1
    makeMove("E1", "D1")
    assert len(wKing.getCastlingRights(board)) == 0

def test_Pawn_enPassant():
    from chupochess.board import Board
    from chupochess.common import Location, File
    board = Board()
    files = [file.name for file in File]
    def makeMove(sFrom: str, sTo: str) -> None:
        # input format: sFrom/sTo = "A8"
        fromSquare = board.locationSquareMap[Location(int(sFrom[1]) - 1, File(files.index(sFrom[0])))]
        toSquare = board.locationSquareMap[Location(int(sTo[1]) - 1, File(files.index(sTo[0])))]
        fromSquare.currentPiece.makeMove(toSquare, board)
    
    # do some moves to allow en passant capture by white:
    makeMove("E2", "E5")
    assert len(board.enPassantPossible) == 1
    makeMove("A7", "A5")
    assert len(board.enPassantPossible) == 1
    makeMove("F1","D3")
    assert len(board.enPassantPossible) == 0
    makeMove("F7", "F5")
    assert len(board.enPassantPossible) == 1
    assert len(board.whitePieces) == 16
    assert len(board.blackPieces) == 16
    makeMove("E5", "F6")    # en passant capture
    assert len(board.enPassantPossible) == 0
    assert len(board.whitePieces) == 16
    assert len(board.blackPieces) == 15
    # same for black:
    makeMove("H7", "H4")
    makeMove("G2", "G4")
    assert len(board.enPassantPossible) == 1
    assert len(board.whitePieces) == 16
    assert len(board.blackPieces) == 15
    makeMove("H4", "G3")
    assert len(board.enPassantPossible) == 0
    assert len(board.whitePieces) == 15
    assert len(board.blackPieces) == 15

def test_possibleMoves_allPieces():
    from typing import Tuple
    from chupochess.board import Board
    from chupochess.common import Location, File
    board = Board()
    files = [file.name for file in File]
    def makeMove(sFrom: str, sTo: str) -> None:
        # input format: sFrom/sTo = "A8"
        fromSquare = board.locationSquareMap[Location(int(sFrom[1]) - 1, File(files.index(sFrom[0])))]
        toSquare = board.locationSquareMap[Location(int(sTo[1]) - 1, File(files.index(sTo[0])))]
        fromSquare.currentPiece.makeMove(toSquare, board)
    def countPossibleMoves() -> Tuple[int, int]:
        cntPieces = 0
        cntMoves = 0
        for piece in board.whitePieces:
            cntMoves += len(piece.getValidMoves(board))
            cntPieces += 1
        for piece in board.blackPieces:
            cntMoves += len(piece.getValidMoves(board))
            cntPieces += 1
        return (cntPieces, cntMoves)

    assert countPossibleMoves() == (32, 40)
    makeMove("H2", "H3")
    assert countPossibleMoves() == (32, 39)
    makeMove("E7","E6")
    assert countPossibleMoves() == (32, 49)
    makeMove("B1", "A3")
    assert countPossibleMoves() == (32, 49)
    makeMove("F8", "C5")
    assert countPossibleMoves() == (32, 53)
    makeMove("D2", "D4")
    assert countPossibleMoves() == (32, 59)
    makeMove("G8", "F6")
    assert countPossibleMoves() == (32, 59)
    makeMove("D4", "C5")
    assert countPossibleMoves() == (31, 55)

def test_board_isInsufficientMaterial():
    from chupochess.board import Board
    from chupochess.common import Location, File
    board = Board()
    files = [file.name for file in File]
    def makeMove(sFrom: str, sTo: str) -> None:
        # input format: sFrom/sTo = "A8"
        fromSquare = board.locationSquareMap[Location(int(sFrom[1]) - 1, File(files.index(sFrom[0])))]
        toSquare = board.locationSquareMap[Location(int(sTo[1]) - 1, File(files.index(sTo[0])))]
        fromSquare.currentPiece.makeMove(toSquare, board)
    
    assert board._isInsufficientMaterial() == False
    makeMove("A1", "A2")
    makeMove("A2", "A7")
    # remove all pawns: 
    for i in range(7):
        makeMove(File(i).name + "7", File(i + 1).name + "2")
        makeMove(File(i + 1).name + "2", File(i + 1).name + "7")
    # --> white rook from A1 is now on H7, no pawns left, everything else is in starting position
    assert board._isInsufficientMaterial() == False
    makeMove("H7", "A8")
    for i in range(3):      # remove (queenside) black knight, bishop and queen
        makeMove(File(i).name + "8", File(i + 1).name + "8")
    makeMove("D8", "F8")
    makeMove("F8", "G8")
    # --> black player only has king and rook left
    assert board._isInsufficientMaterial() == False
    assert len(board.blackPieces) == 2
    
    makeMove("G8", "H1")
    makeMove("H1", "G1")
    makeMove("G1", "F1")
    makeMove("F1", "D1")
    makeMove("D1", "C1")
    assert board._isInsufficientMaterial() == False
    makeMove("B1", "C1")
    assert board._isInsufficientMaterial() == False
    makeMove("H8", "D1")
    makeMove("E1", "D1")
    assert board._isInsufficientMaterial() == True
    makeMove("C1", "F8")
    makeMove("E8", "F8")
    assert board._isInsufficientMaterial() == True
    assert len(board.blackPieces) == 1
    assert len(board.whitePieces) == 1
    
def test_board_updateGameState():
    from chupochess.board import Board
    from chupochess.common import Location, File, GameState
    board = Board()
    files = [file.name for file in File]
    def makeMove(sFrom: str, sTo: str) -> None:
        # input format: sFrom/sTo = "A8"
        fromSquare = board.locationSquareMap[Location(int(sFrom[1]) - 1, File(files.index(sFrom[0])))]
        toSquare = board.locationSquareMap[Location(int(sTo[1]) - 1, File(files.index(sTo[0])))]
        fromSquare.currentPiece.makeMove(toSquare, board)
    
    assert board.gameState == GameState.RUNNING
    board.whiteToMove = False
    board.updateGameState()
    assert board.gameState == GameState.RUNNING
    # checkmate: one piece attacking + no valid moves nowhere:
    makeMove("D1", "F7")
    board.updateGameState()
    assert board.gameState == GameState.RUNNING
    makeMove("H1", "F3")
    board.updateGameState()
    assert board.gameState == GameState.WHITE_WINS
    makeMove("F7", "D1")
    board.gameState = GameState.RUNNING
    board.updateGameState()
    assert board.gameState == GameState.RUNNING
    # checkmate two pieces attacking + no valid moves:
    makeMove("G8", "D3")
    board.whiteToMove = True
    assert board.gameState == GameState.RUNNING
    makeMove("A8", "E2")
    board.updateGameState()
    assert board.gameState == GameState.RUNNING
    makeMove("E2", "E3")
    board.updateGameState()
    assert board.gameState == GameState.BLACK_WINS
    # remove white pawns:
    makeMove("E3", "A2")
    for i in range(7):
        makeMove(File(i).name + "2", File(i + 1).name + "2")
    makeMove("E1", "E2")        # white king now on E2
    # remove all other white pieces:
    makeMove("H2", "A1")
    for i in range(7):
        makeMove(File(i).name + "1", File(i + 1).name + "1")
    makeMove("E2", "E1")        # white king on E1 again
    makeMove("H1", "F3")
    makeMove("F3", "H6")
    # stalemate
    board.gameState = GameState.RUNNING
    board.whiteToMove = True
    board.updateGameState()
    assert board.gameState == GameState.RUNNING
    makeMove("D8", "D3")
    board.updateGameState()
    assert board.gameState == GameState.RUNNING
    makeMove("H6", "F6")
    board.updateGameState()
    assert board.gameState == GameState.DRAW
    # remove all pieces but black rook on H8 with black horse (B2):
    makeMove("B8", "A1")
    src = "A1"
    for row in range(8):
        for col in range(8):
            tar = File(col).name + str(row + 1)
            if tar in ["A1", "E1", "E8", "H8"]:
                continue
            makeMove(src, tar)
            src = tar
    assert len(board.blackPieces) == 3
    assert len(board.whitePieces) == 1
    board.gameState = GameState.RUNNING
    board.updateGameState()
    assert board.gameState == GameState.RUNNING
    # insufficient material:
    makeMove("G8","H8")         # get rid of black rook
    board.updateGameState()
    assert board.gameState == GameState.DRAW

def test_Piece_getGlobalValidMoves():
    from chupochess.board import Board
    from chupochess.common import Location, File
    board = Board()
    files = [file.name for file in File]
    def makeMove(sFrom: str, sTo: str) -> None:
        # input format: sFrom/sTo = "A8"
        fromSquare = board.locationSquareMap[Location(int(sFrom[1]) - 1, File(files.index(sFrom[0])))]
        toSquare = board.locationSquareMap[Location(int(sTo[1]) - 1, File(files.index(sTo[0])))]
        fromSquare.currentPiece.makeMove(toSquare, board)
    def blackPossibleMoves() -> int:
        cntMoves = 0
        for piece in board.blackPieces:
            cntMoves += len(piece.getValidMoves(board))
        return cntMoves

    prepMoves = [("E2","E4"), ("F7","F5"), ("E4", "F5"),("E7","E5"),("F5", "E6"), ("D7", "E6")]
    for move in prepMoves:
        makeMove(move[0], move[1])
    assert len(board.blackPieces) == 14
    assert len(board.whitePieces) == 15
    assert blackPossibleMoves() == 36
    makeMove("F1", "B5")
    assert len(board.blackPieces) == 14
    assert blackPossibleMoves() == 7
    
from typing import List, Tuple
from chupochess.board import Board
from chupochess.common import File, Location, PieceColor

import pygame as p
import sys


class Game:
    def __init__(self):
        self.WIDTH = self.HEIGHT = 400
        self.DIMENSION = 8
        self.SQ_SIZE = self.HEIGHT // self.DIMENSION
        self.MAX_FPS = 15
        self.IMAGES = {}
        self.CLR_DARK_SQ = p.Color(150,180,0)
        self.CLR_LIGHT_SQ = p.Color(240,240,200)
    def uglyMain(self) -> None:
        # TODO: checkmate detection + draw detection
        # -> maybe use the defended locations in case of a check with no possible king movements -> see if the 
        #   attacked path can be blocked or the attacker can be captured (if only one attacker) 
        board = Board()

        files = [file.name for file in File]

        validMoves = None

        while True:
            board.printBoard(validMoves)
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

    def main(self) -> None:
        # TODO: GUI
        # pygame with chess inspiration: https://github.com/mikolaj-skrzypczak/chess-engine/blob/master/chess/ChessMain.py
        p.init()
        board = Board()
        screen = p.display.set_mode((self.WIDTH, self.HEIGHT))
        clock = p.time.Clock()
        screen.fill(p.Color("white"))

        self._loadImages()

        running = True
        squareSelected = None
        highlightedSquares = []         # contains Tuples (Position, p.Color)

        while running:

            self._drawBoard(screen)
            self._drawPieces(screen, board)
            self._highlightSquares(screen, highlightedSquares)

            for e in p.event.get():
                if e.type == p.QUIT:
                    p.quit()
                    sys.exit()
                elif e.type == p.MOUSEBUTTONDOWN:
                    mousePos = tuple(int(pos / self.SQ_SIZE) for pos in p.mouse.get_pos())
                    location = self._getLocation(mousePos)
                    if (squareSelected == None) and (location in board.locationSquareMap) and (board.locationSquareMap[location].isOccupied == True):
                        piece = board.locationSquareMap[location].currentPiece
                        if self._myTurn(board, piece.color):
                            squareSelected = mousePos
                            for move in piece.getValidMoves(board):
                                highlightedSquares.append(self._getPosition(move))
                        else: 
                            squareSelected = None
                            highlightedSquares.clear()
                    elif (squareSelected != None) and (location in board.locationSquareMap) and (mousePos in highlightedSquares):
                        # make move
                        fromSquare = board.locationSquareMap[self._getLocation(squareSelected)]
                        fromSquare.currentPiece.makeMove(board.locationSquareMap[self._getLocation(mousePos)], board)
                        squareSelected = None
                        highlightedSquares.clear()
                    else:
                        squareSelected = None
                        highlightedSquares.clear()
            clock.tick(self.MAX_FPS)
            p.display.flip()

    def _getLocation(self, position: Tuple[int,int]) -> Location:
        # TODO: atm, only for white perspective
        coord = (position[0], abs(position[1] - 7))
        return Location(coord[1], File(coord[0]))

    def _getPosition(self, location: Location) -> Tuple[int, int]: # col, row
        # TODO: atm, only for white perspective
        return (location.file.value, abs(location.rank - 7))

    def _loadImages(self) -> None:
        names = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
        for name in names:
            self.IMAGES[name] = p.transform.scale(p.image.load("static/img/" + name + ".png"), (0.8*self.SQ_SIZE, 0.8*self.SQ_SIZE))

    def _drawBoard(self, screen: p.Surface) -> None:
        global colors
        colors = [self.CLR_LIGHT_SQ, self.CLR_DARK_SQ]
        for row in range(self.DIMENSION):
            for col in range(self.DIMENSION):
                color = colors[((row + col ) % 2)]
                p.draw.rect(screen, color, p.Rect(col * self.SQ_SIZE, row * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))
    
    def _highlightSquares(self, screen: p.Surface, squares: List[Tuple[int,int]]) -> None:
        # input: List[Tuple[Tuple[int,int], p.Color]]
        COLOR = p.Color(255,0,0) 
        for square in squares:
            surface = p.Surface((self.SQ_SIZE, self.SQ_SIZE))
            surface.set_alpha(100)
            surface.fill(COLOR)
            screen.blit(surface, (square[0] * self.SQ_SIZE, square[1] * self.SQ_SIZE))

    def _myTurn(self, board: Board, color: PieceColor) -> bool:
        return (((board.whiteToMove == True) and (color == PieceColor.WHITE)) or ((board.whiteToMove == False) and (color == PieceColor.BLACK)))


    def _drawPieces(self, screen: p.Surface, board: Board):
        # white perspective:
        for piece in board.whitePieces:
            col = piece.currentSquare.location.file.value
            row = abs(piece.currentSquare.location.rank - 7)
            name = "w" + piece.name
            screen.blit(self.IMAGES[name], p.Rect((col+0.1)*self.SQ_SIZE, (row+0.1) * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))

        for piece in board.blackPieces:
            col = piece.currentSquare.location.file.value
            row = abs(piece.currentSquare.location.rank - 7)
            name = "b" + piece.name
            screen.blit(self.IMAGES[name], p.Rect((col+0.1)*self.SQ_SIZE, (row+0.1) * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))






        
from chupochess.board import Board

class Game:
    def __init__(self):
        self.data = "hallo"
        self.board = Board()

    def main(self) -> str:
        return self.board.printBoard()

    
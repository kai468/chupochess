#from chupochess.game import Game

#game = Game()
#game.main()


class Piece:
    def __init__(self, name: str) -> None:
        self.name = name

class Pawn(Piece):
    def __init__(self) -> None:
        super().__init__("P")

class Knight(Piece):
    def __init__(self) -> None:
        super().__init__("N")


def promote(i: int, cls: Piece = Knight):
    x = cls()
    print(x.name)

promote(3, Pawn)
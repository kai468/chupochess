from chupochess.common import SquareColor, Location

class Square:
    def __init__(self, squareColor: SquareColor, location: Location) -> None:
        self.squareColor = squareColor
        self.location = location
        self.isOccupied = False
        self.currentPiece = None 

    def reset(self) -> None:
        self.isOccupied = False
        self.currentPiece = None

    def __str__(self) -> str:
        return "Square{squareColor=" + str(self.squareColor.name) \
            + ",location=" + str(self.location) \
            + ",isOccupied=" + str(self.isOccupied) + "}"
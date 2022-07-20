from enum import Enum

class File(Enum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5
    G = 6
    H = 7

class Location:
    def __init__(self, rank: int, file: File) -> None:
        self.rank = rank
        self.file = file

    def __key(self):
        return (self.rank, self.file)

    def __hash__(self) -> int:
        return hash(self.__key)
        
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Location):
            return self.__key() == __o.__key()
        else:
            return NotImplemented

    def __str__(self) -> str:
        return str(self.file.name) + str(self.rank+1)

class SquareColor(Enum):
    LIGHT = 0
    DARK = 1

class Square:
    def __init__(self, squareColor: SquareColor, location: Location) -> None:
        self.squareColor = squareColor
        self.location = location
        self.isOccupied = False

    def reset(self) -> None:
        self.isOccupied = False

    def __str__(self) -> str:
        return "Square{squareColor=" + str(self.squareColor.name) \
            + ",location=" + str(self.location) \
            + ",isOccupied=" + str(self.isOccupied) + "}"

class Board:
    def __init__(self) -> None:
        self.boardSquares = []
        for file in range(8):
            currentFile = []
            for rank in range(8):
                currentColor = SquareColor(1) if ((file + rank)%2) == 0 else SquareColor(0)
                currentFile.append(Square(currentColor, Location(rank, File(file))))
            self.boardSquares.append(currentFile)

    def printBoard(self) -> str:
        # TODO: what would I use that function for? no information about pieces located on the board
        s = ""
        for file in range(8):
            for rank in range(8):
                s += str(self.boardSquares[file][rank])
            s+="\n"
        return s

            





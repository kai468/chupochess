from enum import Enum

class PieceColor(Enum):
    WHITE = 0
    BLACK = 1

class SquareColor(Enum):
    LIGHT = 0
    DARK = 1

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

class LocationFactory:
    def __init__(self) -> None:
        pass
    def build(location: Location, fileOffset: int, rankOffset: int) -> Location:
        try:
            newLocation = Location(location.rank + rankOffset, File(location.file.value + fileOffset))
            return newLocation
        except:
            return None

class LocationDictionary(dict):
    # TODO: is there a more elegant way to solve this?
    # problem: in operator is not working for Location comparison
    # also getting an item via dict[key] is not working for Location comparison
    # -> __contains__() and __getitem__() must be overwritten 
    def __contains__(self, __o: Location) -> bool:
        for key in self.keys():
            if key == __o: 
                return True
        return False

    def __getitem__(self, __k: Location) -> object:
        for key in self.keys():
            if key == __k:
                return super().__getitem__(key)

    


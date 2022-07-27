#from chupochess.game import Game

#game = Game()
#game.main()


from itertools import filterfalse

# filter out locations that are not on the board:



class C:
    def __init__(self, file: int, isBool: bool, color: str) -> None:
        self.file = file
        self.isBool = isBool
        self.color = color

    def __str__(self) -> str:
        return "C{file=" + str(self.file) +  ";isBool=" + str(self.isBool) + ";color=" + str(self.color) + "}"


moveCandidates = []     # list of candidates

squareMap = {}      # squareMap[location] = square
    # square: .isOccupied = bool
    #            .currentPieceColor = int
# candidate     .file = int

## moveCandidates bsphaft befüllen:
for i in range(10):
    cand = C(i, i%2==0, str(i))
    moveCandidates.append(cand)
    squareMap[cand] = i * 100
currentLocation = C(3, True, "A")


cnt = 0
for key in squareMap.keys().copy():
    if cnt in [3, 7, 9]:
        squareMap.pop(key)
    cnt +=1

for cand in moveCandidates:
    print(cand)

# not in square map:
moveCandidates[:] = filterfalse(lambda candidate : candidate not in squareMap.keys(), moveCandidates)
# move logic:
# same-file moves (no capture) are only allowed if not blocked by other piece:
#moveCandidates[:] = filterfalse(lambda candidate : (candidate.file == currentLocation.file) and (squareMap[candidate].isOccupied == True), moveCandidates)
# captures are only allowed if opponent's piece: 
#moveCandidates[:] = filterfalse(lambda candidate : (candidate.file != currentLocation.file) and (squareMap[candidate].isOccupied == False), moveCandidates)
#moveCandidates[:] = filterfalse(lambda candidate : (candidate.file != currentLocation.file) and (squareMap[candidate].isOccupied == True) and (squareMap[candidate].currentPieceColor == 3), moveCandidates)


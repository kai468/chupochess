class Piece:
    def __init__(self, color):
        self.color = color

    def print_color(self):
        return self.color


class King(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)

class Queen(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)

class Bishop(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)

class Knight(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)

class Rook(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)

class Pawn(Piece):
    def __init__(self, color):
        Piece.__init__(self, color)
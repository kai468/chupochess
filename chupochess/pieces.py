class piece:
    def __init__(self, color):
        self.color = color

    def print_color(self):
        return self.color


class king(piece):
    def __init__(self, color):
        piece.__init__(self, color)

class queen(piece):
    def __init__(self, color):
        piece.__init__(self, color)

class bishop(piece):
    def __init__(self, color):
        piece.__init__(self, color)

class knight(piece):
    def __init__(self, color):
        piece.__init__(self, color)

class rook(piece):
    def __init__(self, color):
        piece.__init__(self, color)

class pawn(piece):
    def __init__(self, color):
        piece.__init__(self, color)
from classes.chess_game import ChessGame

class ReverseMoveFinder:
    def __init__(self, pworkpath):
        self.MyChessGame = ChessGame(pworkpath)

    def GPPN(self):
        """
        Or GeneratePossiblePreviousNodes:
        Generate all potential previous positions that are legal,
        and that transition to current position by one legal move
        """
        pass

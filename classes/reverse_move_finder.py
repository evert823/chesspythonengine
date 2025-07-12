from classes.chess_game import ChessGame
from classes.chess_position import ChessPosition

class ReverseMoveFinder:
    def __init__(self, pworkpath):
        self.MyChessGame = ChessGame(pworkpath)

    def GPPN(self, pposition: ChessPosition):
        """
        Or GeneratePossiblePreviousNodes:
        Generate all potential previous positions that are legal,
        and that transition to current position by one legal move
        """
        for i in range(pposition.boardwidth):
            for j in range(pposition.boardheight):
                if ((pposition.squares[j][i] < 0 and pposition.colourtomove > 0) or
                    (pposition.squares[j][i] > 0 and pposition.colourtomove < 0)):
                    self.handle_piece(pposition, i, j)

    def manipulate_vector(self, pposition: ChessPosition, v):
        #v = input vector coming from piece definition
        #v_c = color dependent vector
        #if white to move then our piece is black and then we flip the sign of y
        if pposition.colourtomove > 0:
            v_c = (v[0], -1 * v[1], v[2])
        else:
            v_c = (v[0], v[1], v[2])
        #v_r = reverse of v_c
        v_r = (-1 * v_c[0], -1 * v_c[1], v_c[2])

        return v_c, v_r

    def handle_piece(self, pposition: ChessPosition, i, j):
        pt = self.MyChessGame.piecetypes[abs(self.squares[j][i]) - 1]

        for v in pt.slidemovevectors:
            v_c, v_r = self.manipulate_vector(pposition, v)
            self.handle_noncapture(pposition, i, j, v_r)
            if pt.IsDivergent == False:
                self.handle_capture(pposition, i, j, v_r)

        if pt.IsDivergent == True:
            for v in pt.slidecapturevectors:
                v_c, v_r = self.manipulate_vector(pposition, v)
                self.handle_capture(pposition, i, j, v_r)



    def handle_noncapture(self, pposition: ChessPosition, i, j, v_r):
        pass

    def handle_capture(self, pposition: ChessPosition, i, j, v_r):
        pass

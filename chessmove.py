import chesshelp

class chessmove:
    def __init__(self, pi1, pj1, pi2, pj2):
        self.MovingPiece = 0
        self.coordinates = (pi1, pj1, pi2, pj2)
        self.IsEnPassant = False
        self.IsCapture = False
        self.IsCastling = False
        #othercoordinates will give the Rook that co-moves with castling, or the pawn captured en passant
        self.othercoordinates = (-1, -1, -1, -1)
        self.PromoteToPiece = 0
    def ShortNotation(self, ppiecetypes):
        if self.IsCastling == True:
            if self.coordinates[2] == 2:
                return "0-0-0"
            else:
                return "0-0"
        s = chesshelp.chesshelp.PieceType2Str(self.MovingPiece, ppiecetypes).replace("-", "")
        s += self.Coord2Squarename(self.coordinates[0], self.coordinates[1])
        if self.IsCapture == True:
            s += "x"
        else:
            s += "-"
        s += self.Coord2Squarename(self.coordinates[2], self.coordinates[3])
        if self.PromoteToPiece != 0:
            s += chesshelp.chesshelp.PieceType2Str(self.PromoteToPiece, ppiecetypes).replace("-", "")
        if self.IsEnPassant == True:
            s += " e.p."
        return s

    def Coord2Squarename(self, pi, pj):
        myalphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        assert pi < 26
        s = myalphabet.lower()[pi]
        s += str(pj + 1)
        return s
#---------------------------------------------------------------------------------------------------------

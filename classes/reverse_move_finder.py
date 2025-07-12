from classes.chess_game import ChessGame
from classes.chess_position import ChessPosition
from classes.chess_move import ChessMove
import copy

class ReverseMoveFinder:
    def __init__(self, pworkpath):
        self.MyChessGame = ChessGame(pworkpath)
        self.cgVerifyer = ChessGame(pworkpath)
        self.PNList : list [tuple[ChessPosition, ChessMove]] = [] #PreviousNodeList

    def GPPN(self, pposition: ChessPosition):
        """
        Or GeneratePossiblePreviousNodes:
        Generate all potential previous positions that are legal,
        and that transition to current position by one legal move
        """
        self.cgVerifyer.mainposition.ResetBoardsize(pposition.boardwidth, pposition.boardheight)
        self.cgVerifyer.piecetypes = copy.deepcopy(self.MyChessGame.piecetypes)

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
        pt = self.MyChessGame.piecetypes[abs(pposition.squares[j][i]) - 1]

        for v in pt.slidemovevectors:
            v_c, v_r = self.manipulate_vector(pposition, v)
            self.handle_noncapture(pposition, i, j, v_r)
            if pt.IsDivergent == False:
                self.handle_capture(pposition, i, j, v_r)

        if pt.IsDivergent == True:
            for v in pt.slidecapturevectors:
                v_c, v_r = self.manipulate_vector(pposition, v)
                self.handle_capture(pposition, i, j, v_r)

    def squares_from_vector(self, pposition: ChessPosition, i, j, v_r):
        squareset = []
        i2 = i + v_r[0]
        j2 = j + v_r[1]
        maxrangecounter = 1

        #The logic with blocked is NOT APPLICABLE when Witch needs to be handled
        blocked = False
        while (i2 >= 0 and i2 < pposition.boardwidth and
                j2 >= 0 and j2 < pposition.boardheight and blocked == False
                and pposition.maxrange_exceeded(maxrangecounter, v_r) == False):
            if pposition.squares[j2][i2] == 0:
                squareset.append((i2, j2))
            else:
                blocked = True

            i2 = i2 + v_r[0]
            j2 = j2 + v_r[1]
            maxrangecounter += 1

        return squareset

    def moves_are_equal(self, mv1: ChessMove, mv2: ChessMove) -> bool:
        if mv1.MovingPiece != mv2.MovingPiece:
            return False
        if mv1.coordinates != mv2.coordinates:
            return False
        if mv1.IsEnPassant != mv2.IsEnPassant:
            return False
        if mv1.IsCapture != mv2.IsCapture:
            return False
        if mv1.IsCastling != mv2.IsCastling:
            return False
        if mv1.othercoordinates != mv2.othercoordinates:
            return False
        if mv1.PromoteToPiece != mv2.PromoteToPiece:
            return False
        return True

    def position_and_move_valid(self, mv: ChessMove) -> bool:
        #PREREQUISITE we have loaded our position into self.cgVerifyer.mainposition
        myval, mymvidx, _ = self.cgVerifyer.Calculation_n_plies(1)
        if self.cgVerifyer.mainposition.POKingIsInCheck() == True:
            return False

        movefound = False
        for movei in range(self.cgVerifyer.mainposition.movelist_totalfound):
            if self.moves_are_equal(self.cgVerifyer.mainposition.movelist[movei], mv):
                movefound = True
                break

        if movefound == False:
            return False

        return True

    def handle_noncapture(self, pposition: ChessPosition, i, j, v_r):
        squareset = self.squares_from_vector(pposition, i, j, v_r)
        for square in squareset:
            i2 = square[0]
            j2 = square[1]
            self.MyChessGame.SynchronizePosition(pposition, self.cgVerifyer.mainposition)
            self.cgVerifyer.mainposition.colourtomove = -1 * pposition.colourtomove
            self.cgVerifyer.mainposition.squares[j2][i2] = pposition.squares[j][i]
            self.cgVerifyer.mainposition.squares[j][i] = 0
            mv = ChessMove(i2, j2, i, j)
            mv.MovingPiece = pposition.squares[j][i]
            if self.position_and_move_valid(mv) == True:
                print(f"Valid node found: {mv.ShortNotation(self.cgVerifyer.piecetypes)}")
                mypos = ChessPosition()
                mypos.ResetBoardsize(pposition.boardwidth, pposition.boardheight)
                self.MyChessGame.SynchronizePosition(self.cgVerifyer.mainposition, mypos)
                self.PNList.append((mypos, mv))

    def handle_capture(self, pposition: ChessPosition, i, j, v_r):
        squareset = self.squares_from_vector(pposition, i, j, v_r)
        for square in squareset:
            i2 = square[0]
            j2 = square[1]
            self.MyChessGame.SynchronizePosition(pposition, self.cgVerifyer.mainposition)
            self.cgVerifyer.mainposition.colourtomove = -1 * pposition.colourtomove
            self.cgVerifyer.mainposition.squares[j2][i2] = pposition.squares[j][i]
            #cpi = captured piece index
            #sq = the captured piece as encoded in squares
            for cpi in range(len(self.cgVerifyer.piecetypes)):
                if self.cgVerifyer.piecetypes[cpi].name != "King":
                    if pposition.colourtomove > 0:
                        sq = cpi + 1
                    else:
                        sq = (cpi + 1) * -1
                    self.cgVerifyer.mainposition.squares[j][i] = sq
                    mv = ChessMove(i2, j2, i, j)
                    mv.MovingPiece = pposition.squares[j][i]
                    mv.IsCapture = True
                    if self.position_and_move_valid(mv) == True:
                        print(f"Valid node found: {mv.ShortNotation(self.cgVerifyer.piecetypes)} captured piece {self.cgVerifyer.piecetypes[cpi].name}")
                        mypos = ChessPosition()
                        mypos.ResetBoardsize(pposition.boardwidth, pposition.boardheight)
                        self.MyChessGame.SynchronizePosition(self.cgVerifyer.mainposition, mypos)
                        self.PNList.append((mypos, mv))

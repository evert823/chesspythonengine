from classes.chess_game import ChessGame
from classes.chess_position import ChessPosition
from classes.chess_move import ChessMove
from classes.chesshelp import chesshelp
import copy

class ReverseMoveFinder:
    def __init__(self, pworkpath, pjsonsourcepath):
        self.MyChessGame = ChessGame(pworkpath, pjsonsourcepath)
        self.cgVerifyer = ChessGame(pworkpath, pjsonsourcepath)
        self.PNList : list [tuple[ChessPosition, ChessMove]] = [] #PreviousNodeList

    def GPPN(self, pposition: ChessPosition):
        """
        Or GeneratePossiblePreviousNodes:
        Generate all potential previous positions that are legal,
        and that transition to current position by one legal move
        """
        self.cgVerifyer.mainposition.ResetBoardsize(pposition.boardwidth, pposition.boardheight)
        self.cgVerifyer.piecetypes = copy.deepcopy(self.MyChessGame.piecetypes)
        self.white_pawn_mpi = chesshelp.Str2PieceType("p", self.cgVerifyer.piecetypes)
        self.black_pawn_mpi = chesshelp.Str2PieceType("-p", self.cgVerifyer.piecetypes)

        for i in range(pposition.boardwidth):
            for j in range(pposition.boardheight):
                if ((pposition.squares[j][i] < 0 and pposition.colourtomove > 0) or
                    (pposition.squares[j][i] > 0 and pposition.colourtomove < 0)):
                    self.handle_piece(pposition, i, j)
                    self.handle_promotion(pposition, i, j)
                    self.handle_castle(pposition, i, j)
                    self.handle_pawn_2move(pposition, i, j)
                    self.handle_enpassant_whitepawn(pposition, i, j)
                    self.handle_enpassant_blackpawn(pposition, i, j)
        self.display_PNList()

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
        mpi = pposition.squares[j][i]
        pt = self.MyChessGame.piecetypes[abs(mpi) - 1]

        for v in pt.slidemovevectors:
            v_c, v_r = self.manipulate_vector(pposition, v)
            self.handle_noncapture(pposition, i, j, v_r, mpi, 0)
            if pt.IsDivergent == False:
                self.handle_capture(pposition, i, j, v_r, mpi, 0)

        if pt.IsDivergent == True:
            for v in pt.slidecapturevectors:
                v_c, v_r = self.manipulate_vector(pposition, v)
                self.handle_capture(pposition, i, j, v_r, mpi, 0)

    def handle_promotion(self, pposition: ChessPosition, i, j):
        if pposition.colourtomove > 0:
            if j != 0:
                return
            mpi = self.black_pawn_mpi
        else:
            if j != pposition.boardheight - 1:
                return
            mpi = self.white_pawn_mpi
        ppi = pposition.squares[j][i]
        ppt = self.MyChessGame.piecetypes[abs(ppi) - 1]
        if ppt.name in ["King", "Pawn"]:
            return

        pt = self.MyChessGame.piecetypes[abs(mpi) - 1]
        #Pls note, we know that the Pawn is divergent
        for v in pt.slidemovevectors:
            v_c, v_r = self.manipulate_vector(pposition, v)
            self.handle_noncapture(pposition, i, j, v_r, mpi, ppi)
        for v in pt.slidecapturevectors:
            v_c, v_r = self.manipulate_vector(pposition, v)
            self.handle_capture(pposition, i, j, v_r, mpi, ppi)

    def handle_castle(self, pposition: ChessPosition, i, j):
        if pposition.colourtomove > 0:
            if j != pposition.boardheight - 1:
                return
        else:
            if j != 0:
                return
        kingside = False
        queenside = False
        if i == pposition.boardwidth - 2:
            kingside = True
        elif i == 2:
            queenside = True
        else:
            return

        mpi = pposition.squares[j][i]
        pt = self.MyChessGame.piecetypes[abs(mpi) - 1]
        if pt.name != "King":
            return
        
        i2 = pposition.boardwidth // 2
        if pposition.squares[j][i2] == 0 or i2 == i:
            pass
        else:
            return
        
        if kingside == True:
            rook_i = i - 1
            rook_i2 = pposition.boardwidth - 1
        elif queenside == True:
            rook_i = i + 1
            rook_i2 = 0

        rook_pi = pposition.squares[j][rook_i]
        rook_pt = self.MyChessGame.piecetypes[abs(rook_pi) - 1]

        if pposition.colourtomove > 0 and rook_pi > 0:
            return
        if pposition.colourtomove < 0 and rook_pi < 0:
            return
        if rook_pt.name != "Rook":
            return
        if pposition.squares[j][rook_i2] != 0:
            return

        self.MyChessGame.SynchronizePosition(pposition, self.cgVerifyer.mainposition)
        self.cgVerifyer.mainposition.colourtomove = -1 * pposition.colourtomove
        self.cgVerifyer.mainposition.squares[j][i] = 0
        self.cgVerifyer.mainposition.squares[j][rook_i] = 0
        self.cgVerifyer.mainposition.squares[j][i2] = mpi
        self.cgVerifyer.mainposition.squares[j][rook_i2] = rook_pi
        if self.cgVerifyer.mainposition.colourtomove > 0:
            self.cgVerifyer.mainposition.whitekinghasmoved = False
            if kingside:
                self.cgVerifyer.mainposition.whitekingsiderookhasmoved = False
            elif queenside:
                self.cgVerifyer.mainposition.whitequeensiderookhasmoved = False
        if self.cgVerifyer.mainposition.colourtomove < 0:
            self.cgVerifyer.mainposition.blackkinghasmoved = False
            if kingside:
                self.cgVerifyer.mainposition.blackkingsiderookhasmoved = False
            elif queenside:
                self.cgVerifyer.mainposition.blackqueensiderookhasmoved = False
        mv = ChessMove(i2, j, i, j)
        mv.MovingPiece = mpi
        mv.IsCastling = True
        mv.othercoordinates = (rook_i2, j, rook_i, j)
        if self.position_and_move_valid(mv) == True:
            mypos = ChessPosition()
            mypos.ResetBoardsize(pposition.boardwidth, pposition.boardheight)
            self.MyChessGame.SynchronizePosition(self.cgVerifyer.mainposition, mypos)
            self.PNList.append((mypos, mv))
        

    def handle_pawn_2move(self, pposition: ChessPosition, i, j):
        mpi = pposition.squares[j][i]
        if pposition.colourtomove > 0:
            if j != pposition.boardheight - 4:
                return
            if mpi != self.black_pawn_mpi:
                return
        else:
            if j != 3:
                return
            if mpi != self.white_pawn_mpi:
                return
        v = (0, 2, 1)
        v_c, v_r = self.manipulate_vector(pposition, v)
        self.handle_noncapture(pposition, i, j, v_r, mpi, 0)

    def handle_enpassant_whitepawn(self, pposition: ChessPosition, i, j):
        if pposition.colourtomove > 0:
            return
        mpi = pposition.squares[j][i]
        if j != pposition.boardheight - 3:
            return
        if mpi != self.white_pawn_mpi:
            return

        pt = self.MyChessGame.piecetypes[abs(mpi) - 1]
        for v in pt.slidecapturevectors:
            v_c, v_r = self.manipulate_vector(pposition, v)
            self.handle_enpassant_capture(pposition, i, j, v_r, mpi)

    def handle_enpassant_blackpawn(self, pposition: ChessPosition, i, j):
        if pposition.colourtomove < 0:
            return
        mpi = pposition.squares[j][i]
        if j != 2:
            return
        if mpi != self.black_pawn_mpi:
            return

        pt = self.MyChessGame.piecetypes[abs(mpi) - 1]
        for v in pt.slidecapturevectors:
            v_c, v_r = self.manipulate_vector(pposition, v)
            self.handle_enpassant_capture(pposition, i, j, v_r, mpi)

    def handle_enpassant_capture(self, pposition: ChessPosition, i, j, v_r, mpi):
        #mpi = moving piece
        squareset = self.squares_from_vector(pposition, i, j, v_r)
        for square in squareset:
            i2 = square[0]
            j2 = square[1]
            self.MyChessGame.SynchronizePosition(pposition, self.cgVerifyer.mainposition)
            self.cgVerifyer.mainposition.colourtomove = -1 * pposition.colourtomove
            self.cgVerifyer.mainposition.squares[j][i] = 0
            self.cgVerifyer.mainposition.squares[j2][i2] = mpi
            sq = mpi * -1
            self.cgVerifyer.mainposition.squares[j2][i] = sq
            self.cgVerifyer.mainposition.precedingmove = (i, j2 - 2 * pposition.colourtomove, i, j2)
            #print(f"precedingmove {self.cgVerifyer.mainposition.precedingmove}")
            mv = ChessMove(i2, j2, i, j)
            mv.MovingPiece = mpi
            mv.IsCapture = True
            mv.IsEnPassant = True
            mv.othercoordinates = (i, j2, -1, -1)
            if self.position_and_move_valid(mv) == True:
                mypos = ChessPosition()
                mypos.ResetBoardsize(pposition.boardwidth, pposition.boardheight)
                self.MyChessGame.SynchronizePosition(self.cgVerifyer.mainposition, mypos)
                self.PNList.append((mypos, mv))

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

    def pawns_on_ranks_valid(self, pposition: ChessPosition) -> bool:
        for i in range(pposition.boardwidth):
            for j in [0, pposition.boardheight - 1]:
                if pposition.squares[j][i] == self.white_pawn_mpi:
                    return False
                if pposition.squares[j][i] == self.black_pawn_mpi:
                    return False
                if pposition.squares[j][i] == self.white_pawn_mpi:
                    return False
                if pposition.squares[j][i] == self.black_pawn_mpi:
                    return False
        return True

    def position_and_move_valid(self, mv: ChessMove) -> bool:
        #PREREQUISITE we have loaded our position into self.cgVerifyer.mainposition

        #TODO check if execute mv from self.cgVerifyer.mainposition --> self.MyChessGame.mainposition

        if self.pawns_on_ranks_valid(self.cgVerifyer.mainposition) == False:
            return False

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

    def handle_noncapture(self, pposition: ChessPosition, i, j, v_r, mpi, ppi):
        #mpi = moving piece, ppi = promoted piece (0 if there is no promotion)

        squareset = self.squares_from_vector(pposition, i, j, v_r)
        for square in squareset:
            i2 = square[0]
            j2 = square[1]
            self.MyChessGame.SynchronizePosition(pposition, self.cgVerifyer.mainposition)
            self.cgVerifyer.mainposition.colourtomove = -1 * pposition.colourtomove
            self.cgVerifyer.mainposition.squares[j2][i2] = mpi
            self.cgVerifyer.mainposition.squares[j][i] = 0
            mv = ChessMove(i2, j2, i, j)
            mv.MovingPiece = mpi
            mv.PromoteToPiece = ppi
            if self.position_and_move_valid(mv) == True:
                mypos = ChessPosition()
                mypos.ResetBoardsize(pposition.boardwidth, pposition.boardheight)
                self.MyChessGame.SynchronizePosition(self.cgVerifyer.mainposition, mypos)
                self.PNList.append((mypos, mv))

    def handle_capture(self, pposition: ChessPosition, i, j, v_r, mpi, ppi):
        #mpi = moving piece, ppi = promoted piece (0 if there is no promotion)

        squareset = self.squares_from_vector(pposition, i, j, v_r)
        for square in squareset:
            i2 = square[0]
            j2 = square[1]
            self.MyChessGame.SynchronizePosition(pposition, self.cgVerifyer.mainposition)
            self.cgVerifyer.mainposition.colourtomove = -1 * pposition.colourtomove
            self.cgVerifyer.mainposition.squares[j2][i2] = mpi
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
                    mv.MovingPiece = mpi
                    mv.PromoteToPiece = ppi
                    mv.IsCapture = True
                    if self.position_and_move_valid(mv) == True:
                        mypos = ChessPosition()
                        mypos.ResetBoardsize(pposition.boardwidth, pposition.boardheight)
                        self.MyChessGame.SynchronizePosition(self.cgVerifyer.mainposition, mypos)
                        self.PNList.append((mypos, mv))

    def display_PNList_item(self, pni):
        s = self.PNList[pni][1].ShortNotation(self.cgVerifyer.piecetypes)
        if self.PNList[pni][1].IsCapture == True:
            s += " captured piece "
            i2 = self.PNList[pni][1].coordinates[2]
            j2 = self.PNList[pni][1].coordinates[3]
            if self.PNList[pni][1].IsEnPassant == True:
                i2 = self.PNList[pni][1].othercoordinates[0]
                j2 = self.PNList[pni][1].othercoordinates[1]
            sq = self.PNList[pni][0].squares[j2][i2]
            pt = self.MyChessGame.piecetypes[abs(sq) - 1]
            s += pt.name
        return s

    def display_PNList(self):
        biglist = []
        for pni in range(len(self.PNList)):
            s = self.display_PNList_item(pni)
            #For now only display non-capture or Queen-capture
            if (s.find("captured piece") < 0 or s.endswith("captured piece Queen")
                or s.endswith("captured piece Pawn")):
                print(s)
            biglist.append(s)
        #print(biglist)

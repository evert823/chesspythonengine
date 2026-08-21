from classes.chess_game import ChessGame
import copy
import random

class RandomPositionGenerator:
    def __init__(self, pworkpath, pjsonsourcepath):
        self.MyChessGame = ChessGame(pworkpath, pjsonsourcepath)
        self.cgVerifyer = ChessGame(pworkpath, pjsonsourcepath)

    def init_verifyer(self):
        self.cgVerifyer.piecetypes = copy.deepcopy(self.MyChessGame.piecetypes)
        self.cgVerifyer.mainposition.ResetBoardsize(self.MyChessGame.mainposition.boardwidth,
                                                    self.MyChessGame.mainposition.boardheight)

    def copy_walls(self, fromgame: ChessGame, togame: ChessGame):
        for j in range(fromgame.mainposition.boardheight):
            for i in range(fromgame.mainposition.boardwidth):
                if fromgame.mainposition.squares[j][i] != 0:
                    pt = fromgame.piecetypes[abs(fromgame.mainposition.squares[j][i]) - 1]
                    if pt.name == "Wall":
                        togame.mainposition.squares[j][i] = fromgame.mainposition.squares[j][i]

    def is_valid_position(self, cg: ChessGame):
        pawns_valid = cg.mainposition.pawns_on_ranks_valid(ppiecetypes=cg.piecetypes)
        if pawns_valid == False:
            return (False, "Invalid pawns found")

        max_one_king = cg.mainposition.max_one_king_per_side(ppiecetypes=cg.piecetypes)
        if max_one_king == False:
            return (False, "More than one King on one of the sides")

        myval, mymvidx, _ = cg.Calculation_n_plies(1)
        if cg.mainposition.POKingIsInCheck() == True:
            return (False, "The King can be taken")

        return (True, f"Evaluation {myval} - There were {cg.mainposition.movelist_totalfound} legal moves")

    def _pick_k(self, k, size):
        n = random.randint(1, 50)
        if k == 0:
            if n <= 35:
                return k
            else:
                return k + 1
        elif k == size - 1:
            if n <= 35:
                return k
            else:
                return k - 1
        else:
            if n <= 30:
                return k
            elif n <= 40:
                return k + 1
            else:
                return k - 1


    def _put_piece_square(self, sqvalue, i, j,
                          toposition, number_of_attempts):
        '''
        Put a desired piece on a target square [j][i]
        Piece given by sqvalue which is negative or positive integer
        Based on probability exactly on or near the target square
        Number of attempts controlled by parameter
        '''
        piece_placed = False
        attempts = 0
        while piece_placed == False and attempts < number_of_attempts:
            attempts += 1
            i2 = self._pick_k(k=i, size=toposition.boardwidth)
            j2 = self._pick_k(k=j, size=toposition.boardheight)
            if toposition.squares[j2][i2] == 0:
                toposition.squares[j2][i2] = sqvalue
                piece_placed = True
        return piece_placed

    def generate_one_position(self):
        self.init_verifyer()
        lost_pieces_count = 0
        self.copy_walls(fromgame=self.MyChessGame, togame=self.cgVerifyer)

        self.cgVerifyer.mainposition.colourtomove = self.MyChessGame.mainposition.colourtomove
        self.cgVerifyer.mainposition.whitekinghasmoved = self.MyChessGame.mainposition.whitekinghasmoved
        self.cgVerifyer.mainposition.whitekingsiderookhasmoved = self.MyChessGame.mainposition.whitekingsiderookhasmoved
        self.cgVerifyer.mainposition.whitequeensiderookhasmoved = self.MyChessGame.mainposition.whitequeensiderookhasmoved
        self.cgVerifyer.mainposition.blackkinghasmoved = self.MyChessGame.mainposition.blackkinghasmoved
        self.cgVerifyer.mainposition.blackkingsiderookhasmoved = self.MyChessGame.mainposition.blackkingsiderookhasmoved
        self.cgVerifyer.mainposition.blackqueensiderookhasmoved = self.MyChessGame.mainposition.blackqueensiderookhasmoved

        for j in range(self.MyChessGame.mainposition.boardheight):
            for i in range(self.MyChessGame.mainposition.boardwidth):
                if self.MyChessGame.mainposition.squares[j][i] != 0:
                    pt = self.MyChessGame.piecetypes[abs(self.MyChessGame.mainposition.squares[j][i]) - 1]
                    if pt.name == "King":
                        piece_placed = self._put_piece_square(sqvalue=self.MyChessGame.mainposition.squares[j][i],
                                            i=i, j=j,
                                            toposition=self.cgVerifyer.mainposition,
                                            number_of_attempts=100)
                        if piece_placed == False:
                            lost_pieces_count += 1
        for j in range(self.MyChessGame.mainposition.boardheight):
            for i in range(self.MyChessGame.mainposition.boardwidth):
                if self.MyChessGame.mainposition.squares[j][i] != 0:
                    pt = self.MyChessGame.piecetypes[abs(self.MyChessGame.mainposition.squares[j][i]) - 1]
                    if pt.name not in ["Wall", "King"]:
                        piece_placed = self._put_piece_square(sqvalue=self.MyChessGame.mainposition.squares[j][i],
                                            i=i, j=j,
                                            toposition=self.cgVerifyer.mainposition,
                                            number_of_attempts=100)
                        if piece_placed == False:
                            lost_pieces_count += 1

        return lost_pieces_count

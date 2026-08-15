from classes.chess_game import ChessGame
from classes.chess_position import ChessPosition
import copy

class RandomPositionGenerator:
    def __init__(self, pworkpath, pjsonsourcepath):
        self.MyChessGame = ChessGame(pworkpath, pjsonsourcepath)
        self.cgVerifyer = ChessGame(pworkpath, pjsonsourcepath)

    def init_verifyer(self):
        self.cgVerifyer.piecetypes = copy.deepcopy(self.MyChessGame.piecetypes)
        self.cgVerifyer.mainposition.ResetBoardsize(self.MyChessGame.mainposition.boardwidth,
                                                    self.MyChessGame.mainposition.boardheight)

    def is_valid_position(self, cg: ChessGame):
        pawns_valid = cg.mainposition.pawns_on_ranks_valid(ppiecetypes=cg.piecetypes)
        if pawns_valid == False:
            print("Invalid pawns found")
            return False

        max_one_king = cg.mainposition.max_one_king_per_side(ppiecetypes=cg.piecetypes)
        if max_one_king == False:
            print("More than one King on one of the sides")
            return False

        myval, mymvidx, _ = cg.Calculation_n_plies(1)
        if cg.mainposition.POKingIsInCheck() == True:
            print("The King can be taken")
            return False

        print(cg.mainposition.movelist_totalfound)

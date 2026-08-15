from classes.chess_game import ChessGame
import copy

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
                pt = fromgame.ppiecetypes[abs(fromgame.mainposition.squares[j][i]) - 1]
                if pt.name == "Wall":
                    togame.mainposition.squares[j][i] = fromgame.mainposition.squares[j][i]

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

    def generate_main(self):
        self.init_verifyer()
        self.copy_walls(fromgame=self.MyChessGame, togame=self.cgVerifyer)

import json
from classes.chess_piecetype import ChessPieceType
from classes.chess_move import ChessMove
from classes.chess_position import ChessPosition
from datetime import datetime

class ChessGame:
    def __init__(self, pworkpath, pjsonsourcepath):
        self.piecetypes = []

        self.mainposition = ChessPosition()
        self.workpath = pworkpath
        self.jsonsourcepath = pjsonsourcepath

        now = datetime.now()
        dt_string = now.strftime("%Y_%m_%d_%H_%M_%S")
        self.logfilename = f"{pworkpath}\\log\\chessgamelog_{dt_string}.log"

        self.presort_when_n_plies_gt = 7
        self.presort_using_n_plies = 3
        self.display_when_n_plies_gt = 8
        self.positionstack_size = 25
        self.positionstack = []
#---------------------------------------------------------------------------------------------------------
    def init_positionstack(self):
        self.positionstack.clear()
        for i in range(self.positionstack_size):
            mypos = ChessPosition()
            mypos.ResetBoardsize(self.mainposition.boardwidth, self.mainposition.boardheight)
            self.positionstack.append(mypos)
        self.SynchronizePosition(self.mainposition, self.positionstack[0])
        self.positionstack[0].precedingmove = self.mainposition.precedingmove
#---------------------------------------------------------------------------------------------------------
    def writelog(self, pmessage):
        file = open(self.logfilename, 'a')
        file.write(pmessage + "\n")
        file.close()
#---------------------------------------------------------------------------------------------------------
    def LoadFromJsonFile(self, pfilename, ppositionfilename):
        #Load from json file and convert to class structure
        gamefile = open(pfilename, 'r')
        gamedict = json.load(gamefile)
        gamefile.close()

        self.piecetypes.clear()
        for p in gamedict["piecetypes"]:
            self.LoadPiece(p, self.workpath, self.jsonsourcepath)

        self.mainposition.LoadFromJsonFile(ppositionfilename, self.piecetypes)
#---------------------------------------------------------------------------------------------------------
    def SaveAsJsonFile(self, pfilename, ppositionfilename):
        #Convert class structure to json and save as json file
        gamefile = open(pfilename, 'w')
        gamedict = {}

        gamedict["piecetypes"] = []
        for p in self.piecetypes:
            gamedict["piecetypes"].append(p.name)

        json.dump(gamedict, gamefile, indent=4)
        gamefile.close()

        self.mainposition.SaveAsJsonFile(ppositionfilename, self.piecetypes)
#---------------------------------------------------------------------------------------------------------
    def LoadPiece(self, ppiecename, pworkpath, pjsonsourcepath):
        mytype = ChessPieceType()
        mytype.LoadFromJsonFile(f"{pjsonsourcepath}\\piecedefinitions\\" + ppiecename + ".json")
        mytype.SaveAsJsonFile(f"{pworkpath}\\piecedefinitions_verify\\" + ppiecename + ".json")
        self.piecetypes.append(mytype)
#---------------------------------------------------------------------------------------------------------
    def SynchronizePosition(self, frompos, topos):
        #boardwidth MUST already be in sync
        #boardheight MUST already be in sync
        topos.colourtomove = frompos.colourtomove
        #topos.precedingmove = frompos.precedingmove
        topos.whitekinghasmoved = frompos.whitekinghasmoved
        topos.whitekingsiderookhasmoved = frompos.whitekingsiderookhasmoved
        topos.whitequeensiderookhasmoved = frompos.whitequeensiderookhasmoved
        topos.blackkinghasmoved = frompos.blackkinghasmoved
        topos.blackkingsiderookhasmoved = frompos.blackkingsiderookhasmoved
        topos.blackqueensiderookhasmoved = frompos.blackqueensiderookhasmoved

        for j in range(frompos.boardheight):
            for i in range(frompos.boardwidth):
                topos.squares[j][i] = frompos.squares[j][i]

        topos.ClearNonPersistent()
#---------------------------------------------------------------------------------------------------------
    def ExecuteMove(self, posidx, pmove):
        newposidx = posidx + 1
        self.SynchronizePosition(self.positionstack[posidx], self.positionstack[newposidx])

        i1 = pmove.coordinates[0]
        j1 = pmove.coordinates[1]
        i2 = pmove.coordinates[2]
        j2 = pmove.coordinates[3]

        self.positionstack[newposidx].precedingmove = (i1, j1, i2, j2)

        if pmove.PromoteToPiece != 0:
            self.positionstack[newposidx].squares[j2][i2] = pmove.PromoteToPiece
        else:
            self.positionstack[newposidx].squares[j2][i2] = pmove.MovingPiece
        self.positionstack[newposidx].squares[j1][i1] = 0

        #Set castling info for new position BEGIN
        pt = self.piecetypes[abs(pmove.MovingPiece) - 1]

        if pt.name == "King":
            if self.positionstack[posidx].colourtomove == 1:
                self.positionstack[newposidx].whitekinghasmoved = True
            else:
                self.positionstack[newposidx].blackkinghasmoved = True
        elif pt.name == "Rook":
            _, i_qr, i_kr = self.positionstack[posidx].LocateKingRooks4Castling(self.piecetypes)
            if self.positionstack[posidx].colourtomove == 1:
                if i1 == i_qr:
                    self.positionstack[newposidx].whitequeensiderookhasmoved = True
                elif i1 == i_kr:
                    self.positionstack[newposidx].whitekingsiderookhasmoved = True
            else:
                if i1 == i_qr:
                    self.positionstack[newposidx].blackqueensiderookhasmoved = True
                elif i1 == i_kr:
                    self.positionstack[newposidx].blackkingsiderookhasmoved = True
        #Set castling info for new position END

        if pmove.IsEnPassant == True:
            io1 = pmove.othercoordinates[0]
            jo1 = pmove.othercoordinates[1]
            self.positionstack[newposidx].squares[jo1][io1] = 0

        if pmove.IsCastling == True:
            io1 = pmove.othercoordinates[0]
            jo1 = pmove.othercoordinates[1]
            io2 = pmove.othercoordinates[2]
            jo2 = pmove.othercoordinates[3]
            otherpiece = self.positionstack[newposidx].squares[jo1][io1]

            if io1 != i2:
                self.positionstack[newposidx].squares[jo1][io1] = 0

            self.positionstack[newposidx].squares[jo2][io2] = otherpiece

        if self.positionstack[posidx].colourtomove == 1:
            self.positionstack[newposidx].colourtomove = -1
        else:
            self.positionstack[newposidx].colourtomove = 1

        return newposidx
#---------------------------------------------------------------------------------------------------------
    def Calculation_n_plies(self, n_plies):
        self.init_positionstack()
        myval, moveidx, checkinfo = self.__Calculation_n_plies(0, -100.0, 100.0, n_plies)

        self.mainposition.SquaresAttackedByPM = self.positionstack[0].SquaresAttackedByPM.copy()
        self.mainposition.SquaresAttackedByPO = self.positionstack[0].SquaresAttackedByPO.copy()
        self.mainposition.whitekingcoord = self.positionstack[0].whitekingcoord
        self.mainposition.blackkingcoord = self.positionstack[0].blackkingcoord
        self.mainposition.movelist_totalfound = self.positionstack[0].movelist_totalfound

        for movei in range(self.positionstack[0].movelist_totalfound):
            self.positionstack[0].SynchronizeChessmove(self.positionstack[0].movelist[movei], self.mainposition.movelist[movei])

        return myval, moveidx, checkinfo
#---------------------------------------------------------------------------------------------------------
    def __Calculation_n_plies(self, posidx, alpha, beta, n_plies):
        #response must be tuple len 3 (x, y, z)
        #x = evaluation float
        #y = chessmove idx relative to movelist
        #z = boolean Yes if opponent's King in check else No

        self.positionstack[posidx].LocateKingsRooks(self.piecetypes)

        evalresult = self.positionstack[posidx].StaticEvaluation(self.piecetypes)

        if evalresult in (-100.0, 100.0):
            return (evalresult, None, False)

        self.positionstack[posidx].ScanAttacked(self.piecetypes)

        if self.positionstack[posidx].POKingIsInCheck() == True:
            if self.positionstack[posidx].colourtomove == 1:
                evalresult = 100.0
            else:
                evalresult = -100.0
            return (evalresult, None, True)

        if n_plies == 0:
            return (evalresult, None, False)

        self.positionstack[posidx].Position2MoveList(self.piecetypes)

        new_alpha = alpha
        new_beta = beta


        #presort BEGIN
        if n_plies > self.presort_when_n_plies_gt:
            if n_plies > self.display_when_n_plies_gt:
                self.writelog(f"List before sorting : {self.positionstack[posidx].DisplayMovelist(self.piecetypes)}")
            movelist2 = []
            for movei in range(self.positionstack[posidx].movelist_totalfound):
                mv = ChessMove(0, 0, 0, 0)
                self.positionstack[posidx].SynchronizeChessmove(self.positionstack[posidx].movelist[movei], mv)
                movelist2.append(mv)
            subresults_presort = []
            for i in range(len(movelist2)):
                newposidx = self.ExecuteMove(posidx, movelist2[i])
                newvalue, _, me_in_check = self.__Calculation_n_plies(newposidx, new_alpha, new_beta, self.presort_using_n_plies)
                #self.writelog(f"Value during presort moveidx {i} movevalue {newvalue}")
                subresults_presort.append((i, newvalue))

            if self.positionstack[posidx].colourtomove == 1:
                res_sorted_presort = sorted(subresults_presort, key=lambda tup: tup[1], reverse=True)
            else:
                res_sorted_presort = sorted(subresults_presort, key=lambda tup: tup[1], reverse=False)

            for i in range(len(res_sorted_presort)):
                self.positionstack[posidx].SynchronizeChessmove(movelist2[res_sorted_presort[i][0]], self.positionstack[posidx].movelist[i])
            if n_plies > self.display_when_n_plies_gt:
                self.writelog(f"List after sorting : {self.positionstack[posidx].DisplayMovelist(self.piecetypes)}")
        #presort END

        subresults = []

        bestmoveidx = -1
        if self.positionstack[posidx].colourtomove == 1:
            bestmovevalue = -120.0
        else:
            bestmovevalue = 120.0

        noescapecheck = True
        for i in range(self.positionstack[posidx].movelist_totalfound):
            if n_plies > self.display_when_n_plies_gt:
                movenotation = self.positionstack[posidx].movelist[i].ShortNotation(self.piecetypes)
                self.writelog(f"{datetime.now()} n_plies {n_plies} checking move {movenotation} alpha {new_alpha} beta {new_beta}")
            newposidx = self.ExecuteMove(posidx, self.positionstack[posidx].movelist[i])
            newvalue, _, me_in_check = self.__Calculation_n_plies(newposidx, new_alpha, new_beta, n_plies - 1)
            if me_in_check == False:
                noescapecheck = False
            subresults.append((i, newvalue))

            if self.positionstack[posidx].colourtomove == 1:
                if newvalue > bestmovevalue:
                    bestmovevalue = newvalue
                    bestmoveidx = i
                if new_alpha < newvalue:
                    new_alpha = newvalue
                if newvalue >= new_beta:
                    break
            else:
                if newvalue < bestmovevalue:
                    bestmovevalue = newvalue
                    bestmoveidx = i
                if new_beta > newvalue:
                    new_beta = newvalue
                if newvalue <= new_alpha:
                    break

        #Mate
        if self.positionstack[posidx].PMKingIsInCheck() == True and noescapecheck == True:
            if self.positionstack[posidx].colourtomove == 1:
                evalresult = -100.0
            else:
                evalresult = 100.0
            return (evalresult, None, False)
        #Stalemate
        if self.positionstack[posidx].PMKingIsInCheck() == False and noescapecheck == True:
            evalresult = 0.0
            return (evalresult, None, False)

        evalresult = bestmovevalue

        return (evalresult, bestmoveidx, False)
#---------------------------------------------------------------------------------------------------------
    def SwapBlackWhite(self, pposition):
        #For testing purposes - create same position with reversed colours and mirrored
        myresultpos = ChessPosition()

        myresultpos.ResetBoardsize(pposition.boardwidth, pposition.boardheight)

        myresultpos.colourtomove = pposition.colourtomove * -1

        if pposition.precedingmove[0] > -1:
            a = (pposition.precedingmove[0], 
                (pposition.boardheight - 1) - pposition.precedingmove[1],
                pposition.precedingmove[2],
                (pposition.boardheight - 1) - pposition.precedingmove[3])
            myresultpos.precedingmove = a

        myresultpos.whitekinghasmoved = pposition.blackkinghasmoved
        myresultpos.whitekingsiderookhasmoved = pposition.blackkingsiderookhasmoved
        myresultpos.whitequeensiderookhasmoved = pposition.blackqueensiderookhasmoved
        myresultpos.blackkinghasmoved = pposition.whitekinghasmoved
        myresultpos.blackkingsiderookhasmoved = pposition.whitekingsiderookhasmoved
        myresultpos.blackqueensiderookhasmoved = pposition.whitequeensiderookhasmoved

        for i in range(myresultpos.boardwidth):
            for j in range(myresultpos.boardheight):
                i2 = i
                j2 = (myresultpos.boardheight - 1) - j
                myresultpos.squares[j][i] = pposition.squares[j2][i2] * -1

        myresultpos.ClearNonPersistent()

        return myresultpos

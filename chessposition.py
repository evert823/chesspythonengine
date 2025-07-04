import json
import chesshelp
from chessmove import chessmove

class chessposition:
    def __init__(self):
        self.boardwidth = -1
        self.boardheight = -1
        self.colourtomove = 1 # 1 for white; -1 for black
        #only purpose of storing preceding move here, is to determine legality of en passant
        self.precedingmove = (-1, -1, -1, -1)
        self.whitekinghasmoved = True
        self.whitekingsiderookhasmoved = True
        self.whitequeensiderookhasmoved = True
        self.blackkinghasmoved = True
        self.blackkingsiderookhasmoved = True
        self.blackqueensiderookhasmoved = True
        self.squares = []
        self.SquaresAttackedByPM = [] #list of squares as tuples (i,j) that the player to move is attacking
        self.SquaresAttackedByPO = [] #list of squares as tuples (i,j) that the opponent is attacking
        self.whitekingcoord = (-1, -1)
        self.whitekingsiderookcoord = (-1, -1)
        self.whitequeensiderookcoord = (-1, -1)
        self.blackkingcoord = (-1, -1)
        self.blackkingsiderookcoord = (-1, -1)
        self.blackqueensiderookcoord = (-1, -1)
        self.movelist_allocated = 500
        self.movelist_totalfound = 0
        self.movelist = []
        self.AllocateMovelist()
#---------------------------------------------------------------------------------------------------------
    def ClearNonPersistent(self):
        self.SquaresAttackedByPM.clear()
        self.SquaresAttackedByPO.clear()
        self.whitekingcoord = (-1, -1)
        self.whitekingsiderookcoord = (-1, -1)
        self.whitequeensiderookcoord = (-1, -1)
        self.blackkingcoord = (-1, -1)
        self.blackkingsiderookcoord = (-1, -1)
        self.blackqueensiderookcoord = (-1, -1)
        self.movelist_totalfound = 0
#---------------------------------------------------------------------------------------------------------
    def ResetBoardsize(self, pboardwidth, pboardheight):
        self.boardwidth = pboardwidth
        self.boardheight = pboardheight
        self.squares.clear()
        for j in range(self.boardheight):
            myrank = []
            for i in range(self.boardwidth):
                myrank.append(0)
            self.squares.append(myrank)
        self.ClearNonPersistent()
#---------------------------------------------------------------------------------------------------------
    def AllocateMovelist(self):
        self.movelist.clear()
        for i in range(self.movelist_allocated):
            mv = chessmove(0, 0, 0, 0)
            self.movelist.append(mv)
#---------------------------------------------------------------------------------------------------------
    def LoadFromJsonFile(self, pfilename, ppiecetypes):
        #Load from json file and convert to class structure
        positionfile = open(pfilename, 'r')
        positiondict = json.load(positionfile)
        positionfile.close()
        self.boardwidth = positiondict["boardwidth"]
        self.boardheight = positiondict["boardheight"]
        self.colourtomove = positiondict["colourtomove"]
        self.ResetBoardsize(self.boardwidth, self.boardheight)

        if "precedingmove" in positiondict:
            self.precedingmove = (positiondict["precedingmove"]["x_from"], positiondict["precedingmove"]["y_from"], 
                                  positiondict["precedingmove"]["x_to"], positiondict["precedingmove"]["y_to"])
        else:
            self.precedingmove = (-1, -1, -1, -1)

        if "castlinginfo" in positiondict:
            self.whitekinghasmoved = positiondict["castlinginfo"]["whitekinghasmoved"]
            self.whitekingsiderookhasmoved = positiondict["castlinginfo"]["whitekingsiderookhasmoved"]
            self.whitequeensiderookhasmoved = positiondict["castlinginfo"]["whitequeensiderookhasmoved"]
            self.blackkinghasmoved = positiondict["castlinginfo"]["blackkinghasmoved"]
            self.blackkingsiderookhasmoved = positiondict["castlinginfo"]["blackkingsiderookhasmoved"]
            self.blackqueensiderookhasmoved = positiondict["castlinginfo"]["blackqueensiderookhasmoved"]
        else:
            self.whitekinghasmoved = True
            self.whitekingsiderookhasmoved = True
            self.whitequeensiderookhasmoved = True
            self.blackkinghasmoved = True
            self.blackkingsiderookhasmoved = True
            self.blackqueensiderookhasmoved = True

        for j in range(self.boardheight):
            rj = (self.boardheight - 1) - j
            mysymbol = positiondict["squares"][rj].split("|")
            for i in range(self.boardwidth):
                s = mysymbol[i].lstrip()
                self.squares[j][i] = chesshelp.chesshelp.Str2PieceType(s, ppiecetypes)
#---------------------------------------------------------------------------------------------------------
    def SaveAsJsonFile(self, pfilename, ppiecetypes):
        #Convert class structure to json and save as json file
        positionfile = open(pfilename, 'w')
        positiondict = {}
        positiondict["boardwidth"] = self.boardwidth
        positiondict["boardheight"] = self.boardheight
        positiondict["colourtomove"] = self.colourtomove

        if self.precedingmove == (-1, -1, -1, -1):
            pass
        else:
            positiondict["precedingmove"] = {"x_from": self.precedingmove[0], "y_from": self.precedingmove[1],
                                             "x_to": self.precedingmove[2], "y_to": self.precedingmove[3]}

        if (self.whitekinghasmoved == False or self.whitekingsiderookhasmoved == False or self.whitequeensiderookhasmoved == False or
            self.blackkinghasmoved == False or self.blackkingsiderookhasmoved == False or self.blackqueensiderookhasmoved == False):
            positiondict["castlinginfo"] = {"whitekinghasmoved": self.whitekinghasmoved, 
                                            "whitekingsiderookhasmoved": self.whitekingsiderookhasmoved,
                                            "whitequeensiderookhasmoved": self.whitequeensiderookhasmoved,
                                            "blackkinghasmoved": self.blackkinghasmoved,
                                            "blackkingsiderookhasmoved": self.blackkingsiderookhasmoved,
                                            "blackqueensiderookhasmoved": self.blackqueensiderookhasmoved}

        positiondict["squares"] = []
        for j in range(self.boardheight):
            rj = (self.boardheight - 1) - j
            myvisualrank = ""
            for i in range(self.boardwidth):
                mysymbol = chesshelp.chesshelp.PieceType2Str(self.squares[rj][i], ppiecetypes)
                while len(mysymbol) < 3:
                    mysymbol = " " + mysymbol
                myvisualrank += mysymbol
                if i < self.boardwidth - 1:
                    myvisualrank += "|"
            positiondict["squares"].append(myvisualrank)

        json.dump(positiondict, positionfile, indent=4)
        positionfile.close()
#---------------------------------------------------------------------------------------------------------
    def PositionFromFEN(self, pfen, ppiecetypes):
        fenparts0 = pfen.split(" ")
        fenparts = fenparts0[0].split("/")
        
        self.boardwidth = 8
        self.boardheight = 8

        if fenparts0[1].lower() == "w":
            self.colourtomove = 1
        else:
            self.colourtomove = -1

        self.ResetBoardsize(self.boardwidth, self.boardheight)
        self.precedingmove = (-1, -1, -1, -1)
        self.whitekinghasmoved = True
        self.whitekingsiderookhasmoved = True
        self.whitequeensiderookhasmoved = True
        self.blackkinghasmoved = True
        self.blackkingsiderookhasmoved = True
        self.blackqueensiderookhasmoved = True

        for j in range(len(fenparts)):
            rj = (self.boardheight - 1) - j
            fp = fenparts[j]
            csqi = 0
            for ci in range(len(fp)):
                if fp[ci].isnumeric() == True:
                    csqi += int(fp[ci])
                else:
                    self.squares[rj][csqi] = chesshelp.chesshelp.Str2PieceType4FEN(fp[ci], ppiecetypes)
                    csqi += 1
#---------------------------------------------------------------------------------------------------------
    def PositionAsFEN(self, ppiecetypes):
        fenparts = []
        for j in range(self.boardheight):
            rj = (self.boardheight - 1) - j
            vacantcount = 0
            fenpart = ""
            for i in range(self.boardwidth):
                if self.squares[rj][i] != 0:
                    if vacantcount != 0:
                        fenpart += str(vacantcount)
                        vacantcount = 0
                    mysymbol = chesshelp.chesshelp.PieceType2Str4FEN(self.squares[rj][i], ppiecetypes)
                    fenpart += mysymbol
                if self.squares[rj][i] == 0:
                    vacantcount += 1
            if vacantcount != 0:
                fenpart += str(vacantcount)
            fenparts.append(fenpart)
        fen = "/".join(fenparts)
        if self.colourtomove == 1:
            fen += " w"
        else:
            fen += " b"
        return fen
#---------------------------------------------------------------------------------------------------------
    def WhiteKingIsInCheck(self):
        if self.colourtomove == 1:
            if self.whitekingcoord in self.SquaresAttackedByPO:
                return True
        else:
            if self.whitekingcoord in self.SquaresAttackedByPM:
                return True
        return False
#---------------------------------------------------------------------------------------------------------
    def BlackKingIsInCheck(self):
        if self.colourtomove == 1:
            if self.blackkingcoord in self.SquaresAttackedByPM:
                return True
        else:
            if self.blackkingcoord in self.SquaresAttackedByPO:
                return True
        return False
#---------------------------------------------------------------------------------------------------------
    def PMKingIsInCheck(self):
        if self.colourtomove == 1:
            if self.whitekingcoord in self.SquaresAttackedByPO:
                return True
        else:
            if self.blackkingcoord in self.SquaresAttackedByPO:
                return True
        return False
#---------------------------------------------------------------------------------------------------------
    def POKingIsInCheck(self):
        if self.colourtomove == 1:
            if self.blackkingcoord in self.SquaresAttackedByPM:
                return True
        else:
            if self.whitekingcoord in self.SquaresAttackedByPM:
                return True
        return False
#---------------------------------------------------------------------------------------------------------
    def ScanAttacked(self, ppiecetypes):
        SquaresAttackedByPMdup = []
        SquaresAttackedByPOdup = []
        for i in range(self.boardwidth):
            for j in range(self.boardheight):
                if ((self.squares[j][i] > 0 and self.colourtomove > 0) or
                    (self.squares[j][i] < 0 and self.colourtomove < 0)):
                    SquaresAttackedByPMdup.extend(self.GetSlideAttacks(i, j, ppiecetypes))
                if ((self.squares[j][i] > 0 and self.colourtomove < 0) or
                    (self.squares[j][i] < 0 and self.colourtomove > 0)):
                    SquaresAttackedByPOdup.extend(self.GetSlideAttacks(i, j, ppiecetypes))
        self.SquaresAttackedByPM = []
        for x in SquaresAttackedByPMdup:
            if x not in self.SquaresAttackedByPM:
                self.SquaresAttackedByPM.append(x)
        self.SquaresAttackedByPO = []
        for x in SquaresAttackedByPOdup:
            if x not in self.SquaresAttackedByPO:
                self.SquaresAttackedByPO.append(x)
#---------------------------------------------------------------------------------------------------------
    def maxrange_exceeded(self, maxrangecounter, v):
        #v[2] is the maxrange
        if v[2] < 1:
            return False
        if maxrangecounter <= v[2]:
            return False
        return True
#---------------------------------------------------------------------------------------------------------
    def GetSlideAttacks(self, i, j, ppiecetypes):
        SquaresAttacked = []
        pt = ppiecetypes[abs(self.squares[j][i]) - 1]

        if pt.IsDivergent == False:
            lookatvectors = pt.slidemovevectors
        else:
            lookatvectors = pt.slidecapturevectors

        for v in lookatvectors:
            i2 = i + v[0]

            if self.squares[j][i] > 0:
                j2 = j + v[1]
            else:
                j2 = j - v[1]
            maxrangecounter = 1

            blocked = False
            while (i2 >= 0 and i2 < self.boardwidth and
                   j2 >= 0 and j2 < self.boardheight and blocked == False
                   and self.maxrange_exceeded(maxrangecounter, v) == False):
                
                SquaresAttacked.append((i2, j2))

                if self.squares[j2][i2] != 0:
                    blocked = True

                i2 = i2 + v[0]

                if self.squares[j][i] > 0:
                    j2 = j2 + v[1]
                else:
                    j2 = j2 - v[1]
                maxrangecounter += 1
        return SquaresAttacked
#---------------------------------------------------------------------------------------------------------
    def InitializeMove(self, movei, pi1, pj1, pi2, pj2):
        self.movelist[movei].MovingPiece = 0
        self.movelist[movei].coordinates = (pi1, pj1, pi2, pj2)
        self.movelist[movei].IsEnPassant = False
        self.movelist[movei].IsCapture = False
        self.movelist[movei].IsCastling = False
        self.movelist[movei].othercoordinates = (-1, -1, -1, -1)
        self.movelist[movei].PromoteToPiece = 0
#---------------------------------------------------------------------------------------------------------
    def SynchronizeChessmove(self, frommove, tomove):
        tomove.MovingPiece = frommove.MovingPiece
        tomove.coordinates = frommove.coordinates
        tomove.IsEnPassant = frommove.IsEnPassant
        tomove.IsCapture = frommove.IsCapture
        tomove.IsCastling = frommove.IsCastling
        tomove.othercoordinates = frommove.othercoordinates
        tomove.PromoteToPiece = frommove.PromoteToPiece
#---------------------------------------------------------------------------------------------------------
    def Position2MoveList(self, ppiecetypes):
        self.movelist_totalfound = 0
        for i in range(self.boardwidth):
            for j in range(self.boardheight):
                if ((self.squares[j][i] > 0 and self.colourtomove > 0) or
                    (self.squares[j][i] < 0 and self.colourtomove < 0)):
                    self.GetSlideMoves(i, j, ppiecetypes)
                    self.GetSlideCaptures(i, j, ppiecetypes)
                    self.GetPawn2StepMoves(ppiecetypes, i, j)
                    self.GetPawnEnPassantMoves(ppiecetypes, i, j)
        self.GetCastling(ppiecetypes)
#---------------------------------------------------------------------------------------------------------
    def DisplayMovelist(self, ppiecetypes):
        sl = []
        for movei in range(self.movelist_totalfound):
            sl.append(self.movelist[movei].ShortNotation(ppiecetypes))
        s = ",".join(sl)
        return s
#---------------------------------------------------------------------------------------------------------
    def GetSlideMoves(self, i, j, ppiecetypes):
        #print(f"GetSlideMoves({i},{j})")

        pt = ppiecetypes[abs(self.squares[j][i]) - 1]
        
        for v in pt.slidemovevectors:
            i2 = i + v[0]

            if self.colourtomove == 1:
                j2 = j + v[1]
            else:
                j2 = j - v[1]
            maxrangecounter = 1

            blocked = False
            while (i2 >= 0 and i2 < self.boardwidth and
                   j2 >= 0 and j2 < self.boardheight and blocked == False
                   and self.maxrange_exceeded(maxrangecounter, v) == False):
                if self.squares[j2][i2] == 0:
                    movei = self.movelist_totalfound
                    self.InitializeMove(movei, i, j, i2, j2)
                    self.movelist[movei].MovingPiece = self.squares[j][i]
                    self.GetPromotion(movei, ppiecetypes)
                else:
                    blocked = True

                i2 = i2 + v[0]

                if self.colourtomove == 1:
                    j2 = j2 + v[1]
                else:
                    j2 = j2 - v[1]
                maxrangecounter += 1
#---------------------------------------------------------------------------------------------------------
    def GetSlideCaptures(self, i, j, ppiecetypes):
        #print(f"GetSlideCaptures({i},{j})")

        pt = ppiecetypes[abs(self.squares[j][i]) - 1]

        if pt.IsDivergent == False:
            lookatvectors = pt.slidemovevectors
        else:
            lookatvectors = pt.slidecapturevectors

        for v in lookatvectors:
            i2 = i + v[0]

            if self.colourtomove == 1:
                j2 = j + v[1]
            else:
                j2 = j - v[1]
            maxrangecounter = 1

            blocked = False
            while (i2 >= 0 and i2 < self.boardwidth and
                   j2 >= 0 and j2 < self.boardheight and blocked == False
                   and self.maxrange_exceeded(maxrangecounter, v) == False):

                if ((self.squares[j2][i2] > 0 and self.squares[j][i] < 0) or
                    (self.squares[j2][i2] < 0 and self.squares[j][i] > 0)):
                    movei = self.movelist_totalfound
                    self.InitializeMove(movei, i, j, i2, j2)
                    self.movelist[movei].MovingPiece = self.squares[j][i]
                    self.movelist[movei].IsCapture = True
                    self.GetPromotion(movei, ppiecetypes)
                    blocked = True
                elif self.squares[j2][i2] != 0:
                    blocked = True

                i2 = i2 + v[0]

                if self.colourtomove == 1:
                    j2 = j2 + v[1]
                else:
                    j2 = j2 - v[1]
                maxrangecounter += 1
#---------------------------------------------------------------------------------------------------------
    def GetPromotion(self, movei, ppiecetypes):
        includepromote = False
        includenonpromote = False

        pt1 = ppiecetypes[abs(self.movelist[movei].MovingPiece) - 1]

        if pt1.name in ["Pawn"]:
            if self.movelist[movei].MovingPiece > 0 and self.movelist[movei].coordinates[3] == self.boardheight - 1:
                includepromote = True
                includenonpromote = False
            elif self.movelist[movei].MovingPiece < 0 and self.movelist[movei].coordinates[3] == 0:
                includepromote = True
                includenonpromote = False
            else:
                includepromote = False
                includenonpromote = True
        else:
            includepromote = False
            includenonpromote = True

        if includenonpromote == True:
            self.movelist_totalfound += 1

        if includepromote == True:
            for pi in range(len(ppiecetypes)):
                if (ppiecetypes[pi].name not in ["Amazon", "King", pt1.name]):
                    movei2 = self.movelist_totalfound
                    self.SynchronizeChessmove(self.movelist[movei], self.movelist[movei2])
                    if self.movelist[movei].MovingPiece < 0:
                        self.movelist[movei2].PromoteToPiece = (pi + 1) * -1
                    else:
                        self.movelist[movei2].PromoteToPiece = pi + 1
                    self.movelist_totalfound += 1
#---------------------------------------------------------------------------------------------------------
    def GetPawn2StepMoves(self, ppiecetypes, i, j):
        pt = ppiecetypes[abs(self.squares[j][i]) - 1]

        if pt.name != "Pawn":
            return
        if self.colourtomove > 0 and j != 1:
            return
        if self.colourtomove < 0 and j != self.boardheight - 2:
            return

        i2 = i
        i_skip = i
        if self.colourtomove > 0:
            j_skip = j + 1
            j2 = j + 2
        else:
            j_skip = j - 1
            j2 = j - 2
        if self.squares[j_skip][i_skip] == 0 and self.squares[j2][i2] == 0:
            movei = self.movelist_totalfound
            self.InitializeMove(movei, i, j, i2, j2)
            self.movelist[movei].MovingPiece = self.squares[j][i]
            self.movelist_totalfound += 1
#---------------------------------------------------------------------------------------------------------
    def GetPawnEnPassantMoves(self, ppiecetypes, i, j):
        pt = ppiecetypes[abs(self.squares[j][i]) - 1]

        if pt.name != "Pawn":
            return
        if self.precedingmove[3] != j:
            return

        x_from = self.precedingmove[0]
        y_from = self.precedingmove[1]
        x_to = self.precedingmove[2]
        y_to = self.precedingmove[3]
        ptm = ppiecetypes[abs(self.squares[y_to][x_to]) - 1]
        if ptm.name != "Pawn":
            return
        if x_from - i == 1 or x_from - i == -1:
            pass
        else:
            return
        
        if self.colourtomove > 0:
            if self.squares[y_to][x_to] > 0:
                return
            if j != self.boardheight - 4:
                return
            if y_from != y_to + 2:
                return
            movei = self.movelist_totalfound
            self.InitializeMove(movei, i, j, x_from, y_to + 1)
            self.movelist[movei].MovingPiece = self.squares[j][i]
            self.movelist[movei].IsEnPassant = True
            self.movelist[movei].othercoordinates = (x_to, y_to, -1, -1)
            self.movelist[movei].IsCapture = True
            self.movelist_totalfound += 1

        if self.colourtomove < 0:
            if self.squares[y_to][x_to] < 0:
                return
            if j != 3:
                return
            if y_from != y_to - 2:
                return
            movei = self.movelist_totalfound
            self.InitializeMove(movei, i, j, x_from, y_to - 1)
            self.movelist[movei].MovingPiece = self.squares[j][i]
            self.movelist[movei].IsEnPassant = True
            self.movelist[movei].othercoordinates = (x_to, y_to, -1, -1)
            self.movelist[movei].IsCapture = True
            self.movelist_totalfound += 1
#---------------------------------------------------------------------------------------------------------
    def LocateKingsRooks(self, ppiecetypes):
        #If we go from left to right then we should find queensiderooks first
        for i in range(self.boardwidth):
            for j in range(self.boardheight):
                if self.squares[j][i] != 0:
                    pt = ppiecetypes[abs(self.squares[j][i]) - 1]
                    if pt.name == "King":
                        if self.squares[j][i] > 0:
                            self.whitekingcoord = (i, j)
                        else:
                            self.blackkingcoord = (i, j)
                    if pt.name == "Rook":
                        if self.squares[j][i] > 0:
                            if self.whitequeensiderookcoord == (-1, -1) and self.whitekingcoord == (-1, -1):
                                self.whitequeensiderookcoord = (i, j)
                            else:
                                self.whitekingsiderookcoord = (i, j)
                        else:
                            if self.blackqueensiderookcoord == (-1, -1) and self.blackkingcoord == (-1, -1):
                                self.blackqueensiderookcoord = (i, j)
                            else:
                                self.blackkingsiderookcoord = (i, j)
#---------------------------------------------------------------------------------------------------------
    def LocateKingRooks4Castling(self, ppiecetypes):
        if self.colourtomove == 1:
            i_k = self.whitekingcoord[0]
            i_qr = self.whitequeensiderookcoord[0]
            i_kr = self.whitekingsiderookcoord[0]
        elif self.colourtomove == -1:
            i_k = self.blackkingcoord[0]
            i_qr = self.blackqueensiderookcoord[0]
            i_kr = self.blackkingsiderookcoord[0]
        return i_k, i_qr, i_kr
#---------------------------------------------------------------------------------------------------------
    def GetCastling(self, ppiecetypes):
        if self.colourtomove == 1:
            if self.whitekinghasmoved == True:
                return
            j = 0
            if self.whitekingcoord[1] != j:
                return
        if self.colourtomove == -1:
            if self.blackkinghasmoved == True:
                return
            j = self.boardheight - 1
            if self.blackkingcoord[1] != j:
                return


        #Now locate King and Rooks
        i_k, i_qr, i_kr = self.LocateKingRooks4Castling(ppiecetypes)

        queensidepossible = True
        kingsidepossible = True

        if self.colourtomove == 1 and self.whitequeensiderookcoord[1] != j:
            queensidepossible = False
        if self.colourtomove == -1 and self.blackqueensiderookcoord[1] != j:
            queensidepossible = False
        if self.colourtomove == 1 and self.whitekingsiderookcoord[1] != j:
            kingsidepossible = False
        if self.colourtomove == -1 and self.blackkingsiderookcoord[1] != j:
            kingsidepossible = False

        if self.colourtomove == 1 and self.whitequeensiderookhasmoved == True:
            queensidepossible = False
        if self.colourtomove == -1 and self.blackqueensiderookhasmoved == True:
            queensidepossible = False
        if self.colourtomove == 1 and self.whitekingsiderookhasmoved == True:
            kingsidepossible = False
        if self.colourtomove == -1 and self.blackkingsiderookhasmoved == True:
            kingsidepossible = False

        if i_qr > -1 and i_k > i_qr:
            pass
        else:
            queensidepossible = False

        if i_k > -1 and i_kr > i_k:
            pass
        else:
            kingsidepossible = False


        if queensidepossible:
            i_k_new = 2
            i_qr_new = i_k_new + 1
            for i in range(self.boardwidth):
                if ((i > i_qr and i <= i_qr_new) or (i < i_qr and i >= i_qr_new)) and i != i_k:
                    if self.squares[j][i] != 0:
                        queensidepossible = False
                if ((i > i_k and i <= i_k_new) or (i < i_k and i >= i_k_new)) and i != i_qr:
                    if self.squares[j][i] != 0:
                        queensidepossible = False
                if ((i >= i_k and i <= i_k_new) or (i <= i_k and i >= i_k_new)) and (i,j) in self.SquaresAttackedByPO:
                    queensidepossible = False

        if queensidepossible:
            movei = self.movelist_totalfound
            self.InitializeMove(movei, i_k, j, i_k_new, j)
            self.movelist[movei].MovingPiece = self.squares[j][i_k]
            self.movelist[movei].IsCastling = True
            self.movelist[movei].othercoordinates = (i_qr, j, i_qr_new, j)
            self.movelist_totalfound += 1

        if kingsidepossible:
            i_k_new = self.boardwidth - 2
            i_kr_new = i_k_new - 1
            for i in range(self.boardwidth):
                if ((i > i_kr and i <= i_kr_new) or (i < i_kr and i >= i_kr_new)) and i != i_k:
                    if self.squares[j][i] != 0:
                        kingsidepossible = False
                if ((i > i_k and i <= i_k_new) or (i < i_k and i >= i_k_new)) and i != i_kr:
                    if self.squares[j][i] != 0:
                        kingsidepossible = False
                if ((i >= i_k and i <= i_k_new) or (i <= i_k and i >= i_k_new)) and (i,j) in self.SquaresAttackedByPO:
                    kingsidepossible = False

        if kingsidepossible:
            movei = self.movelist_totalfound
            self.InitializeMove(movei, i_k, j, i_k_new, j)
            self.movelist[movei].MovingPiece = self.squares[j][i_k]
            self.movelist[movei].IsCastling = True
            self.movelist[movei].othercoordinates = (i_kr, j, i_kr_new, j)
            self.movelist_totalfound += 1
#---------------------------------------------------------------------------------------------------------
    def StaticEvaluation(self, ppiecetypes):
        if self.whitekingcoord[0] == -1 and self.blackkingcoord[0] == -1:
            myresult = -100.0 * self.colourtomove
            return myresult
        if self.whitekingcoord[0] == -1:
            myresult = -100.0
            return myresult
        if self.blackkingcoord[0] == -1:
            myresult = 100.0
            return myresult

        materialbalance = 0.0
        myresult = 0.0

        for j in range(self.boardheight -1,-1,-1):
            for i in range(self.boardheight):
                if self.squares[j][i] != 0:
                    pi = abs(self.squares[j][i]) - 1
                    pt = ppiecetypes[pi]

                    if self.squares[j][i] > 0:
                        if pt.name == "King":
                            pass
                        else:
                            materialbalance += chesshelp.chesshelp.PieceType2Value(pi, ppiecetypes)
                    else:
                        if pt.name == "King":
                            pass
                        else:
                            materialbalance -= chesshelp.chesshelp.PieceType2Value(pi, ppiecetypes)

        if materialbalance > 8:
            myresult = 80.0
            return myresult
        if materialbalance < -8:
            myresult = -80.0
            return myresult
        return materialbalance * 10
#---------------------------------------------------------------------------------------------------------

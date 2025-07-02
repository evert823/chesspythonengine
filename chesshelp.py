class chesshelp:
    @staticmethod
    def Str2PieceType(psymbol, ppiecetypes):
        for i in range(len(ppiecetypes)):
            if psymbol == ppiecetypes[i].symbol:
                return i + 1
            if psymbol == "-" + ppiecetypes[i].symbol:
                return (i + 1) * -1
        return 0
#---------------------------------------------------------------------------------------------------------
    @staticmethod
    def PieceType2Str(ptypenr, ppiecetypes):
        if ptypenr > 0:
            i = ptypenr - 1
            return ppiecetypes[i].symbol
        if ptypenr < 0:
            i = (ptypenr * -1) - 1
            return "-" + ppiecetypes[i].symbol
        return "."
#---------------------------------------------------------------------------------------------------------
    @staticmethod
    def PieceType2Str4FEN(ptypenr, ppiecetypes):
        if ptypenr > 0:
            i = ptypenr - 1
            return ppiecetypes[i].symbol.upper()
        if ptypenr < 0:
            i = (ptypenr * -1) - 1
            return ppiecetypes[i].symbol.lower()
        return ""
#---------------------------------------------------------------------------------------------------------
    @staticmethod
    def Str2PieceType4FEN(psymbol, ppiecetypes):
        for i in range(len(ppiecetypes)):
            if psymbol == ppiecetypes[i].symbol.upper():
                return i + 1
            if psymbol == ppiecetypes[i].symbol.lower():
                return (i + 1) * -1
        return 0
#---------------------------------------------------------------------------------------------------------
    @staticmethod
    def PieceType2Value(ptypenr, ppiecetypes):
        if ppiecetypes[ptypenr].name == "King":
            myvalue = 1000.0
        elif ppiecetypes[ptypenr].name == "Queen":
            myvalue = 9.1
        elif ppiecetypes[ptypenr].name == "Rook":
            myvalue = 5.0
        elif ppiecetypes[ptypenr].name == "Bishop":
            myvalue = 3.01
        elif ppiecetypes[ptypenr].name == "Knight":
            myvalue = 3.0
        elif ppiecetypes[ptypenr].name == "Pawn":
            myvalue = 1.0
        elif ppiecetypes[ptypenr].name == "Archbishop":
            myvalue = 8.3
        elif ppiecetypes[ptypenr].name == "Chancellor":
            myvalue = 8.4
        elif ppiecetypes[ptypenr].name == "Guard":
            myvalue = 4.0
        elif ppiecetypes[ptypenr].name == "Hunter":
            myvalue = 3.9
        else:
            myvalue = 2.05
        return myvalue
#---------------------------------------------------------------------------------------------------------

import json

class chesspiecetype:
    def __init__(self):
        self.symbol = ''
        self.name = ''
        self.IsDivergent = False
        #Rule: if IsDivergent is false then capturevectors will be ignored, only movevectors will be looked at
        self.CheckDuplicateMoves = False
        self.EstimatedValue = 0.0
        self.stepleapmovevectors = []
        self.slidemovevectors = []
        self.stepleapcapturevectors = []
        self.slidecapturevectors = []
#---------------------------------------------------------------------------------------------------------
    def VectorSetFromjson(self, mydict):
        myresult = []
        for v in mydict:
            myx = v["x"]
            myy = v["y"]
            try:
                mymaxrange = v["maxrange"]
            except:
                mymaxrange = 0
            myresult.append((myx, myy, mymaxrange))
        return myresult
#---------------------------------------------------------------------------------------------------------
    def VectorSetTojson(self, myset):
        myresult = []
        for v in myset:
            vectordict = {}
            vectordict["x"] = v[0]
            vectordict["y"] = v[1]
            vectordict["maxrange"] = v[2]
            myresult.append(vectordict)
        return myresult
#---------------------------------------------------------------------------------------------------------
    def LoadFromJsonFile(self, pfilename):
        #Load from json file and convert to class structure
        piecefile = open(pfilename, 'r')
        piecedict = json.load(piecefile)
        piecefile.close()
        self.symbol = piecedict["symbol"]
        self.name = piecedict["name"]
        self.IsDivergent = piecedict["IsDivergent"]
        self.CheckDuplicateMoves = piecedict["CheckDuplicateMoves"]
        self.EstimatedValue = piecedict["EstimatedValue"]

        self.stepleapmovevectors = self.VectorSetFromjson(piecedict["stepleapmovevectors"]).copy()
        self.slidemovevectors = self.VectorSetFromjson(piecedict["slidemovevectors"]).copy()
        if self.IsDivergent == True:
            self.stepleapcapturevectors = self.VectorSetFromjson(piecedict["stepleapcapturevectors"]).copy()
            self.slidecapturevectors = self.VectorSetFromjson(piecedict["slidecapturevectors"]).copy()
#---------------------------------------------------------------------------------------------------------
    def SaveAsJsonFile(self, pfilename):
        #Convert class structure to json and save as json file
        piecefile = open(pfilename, 'w')
        piecedict = {}
        piecedict["symbol"] = self.symbol
        piecedict["name"] = self.name
        piecedict["IsDivergent"] = self.IsDivergent
        piecedict["CheckDuplicateMoves"] = self.CheckDuplicateMoves
        piecedict["EstimatedValue"] = self.EstimatedValue

        #piecedict["stepleapmovevectors"] = self.VectorSetTojson(self.stepleapmovevectors).copy()
        piecedict["slidemovevectors"] = self.VectorSetTojson(self.slidemovevectors).copy()
        if self.IsDivergent == True:
            #piecedict["stepleapcapturevectors"] = self.VectorSetTojson(self.stepleapcapturevectors).copy()
            piecedict["slidecapturevectors"] = self.VectorSetTojson(self.slidecapturevectors).copy()

        json.dump(piecedict, piecefile, indent=4)
        piecefile.close()
#---------------------------------------------------------------------------------------------------------

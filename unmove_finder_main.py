from classes.unmove_finder import UnmoveFinder
import os

def Test_GenerateUnmoves(mypositionfilename):
    print(f"mypositionfilename {mypositionfilename}")

    umf = UnmoveFinder(myworkpath, myjsonsourcepath)
    umf.PiecelistForUncapture = ["Knight"] #Default ["Bishop"]
    umf.MyChessGame.LoadFromJsonFile(os.path.join(myjsonsourcepath, "games", "guardendgame.json"),
                                     os.path.join(myworkpath, "positions", f"{mypositionfilename}.json"))
    umf.MyChessGame.SaveAsJsonFile(os.path.join(myworkpath, "games_verify", "guardendgame.json"),
                                   os.path.join(myworkpath, "positions_verify", f"{mypositionfilename}.json"))

    umf.GenerateUnmoves(pposition=umf.MyChessGame.mainposition,
                        pfilepath=os.path.join(myworkpath, "predecessorpositions", "fen.txt"),
                        verbose=False)

myworkpath = os.path.join(os.sep, "home", "administrator", "pythonwork")
myjsonsourcepath = os.path.join(os.sep, "home", "administrator", "chesspython")
Test_GenerateUnmoves("crazymate")

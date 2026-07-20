from classes.reverse_move_finder import ReverseMoveFinder
import os

def Test_GPPN(mypositionfilename):
    print(f"mypositionfilename {mypositionfilename}")

    rmf = ReverseMoveFinder(myworkpath, myjsonsourcepath)
    rmf.MyChessGame.LoadFromJsonFile(os.path.join(myjsonsourcepath, "games", "unittestgame.json"),
                                     os.path.join(myworkpath, "positions", f"{mypositionfilename}.json"))
    rmf.MyChessGame.SaveAsJsonFile(os.path.join(myworkpath, "games_verify", "unittestgame.json"),
                                   os.path.join(myworkpath, "positions_verify", f"{mypositionfilename}.json"))

    rmf.GPPN(rmf.MyChessGame.mainposition)

#myworkpath = os.path.join(os.sep, "home", "administrator", "pythonwork")
myworkpath = os.path.join("C:\\", "Users", "Evert Jan", "pythonprojects", "chesspython_nogithub")
myjsonsourcepath = os.path.join("C:\\", "Users", "Evert Jan", "Documents", "GitHub", "chesspython")
Test_GPPN("fide_fun")

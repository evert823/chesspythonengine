from classes.reverse_move_finder import ReverseMoveFinder
import os

def Test_GPPN(mypositionfilename):
    print(f"mypositionfilename {mypositionfilename}")

    rmf = ReverseMoveFinder(myworkpath, myjsonsourcepath)
    rmf.MyChessGame.LoadFromJsonFile(f"{myjsonsourcepath}\\games\\unittestgame.json",
                                     f"{myworkpath}\\positions\\{mypositionfilename}.json")
    rmf.MyChessGame.SaveAsJsonFile(f"{myworkpath}\\games_verify\\unittestgame.json",
                                   f"{myworkpath}\\positions_verify\\{mypositionfilename}.json")

    rmf.GPPN(rmf.MyChessGame.mainposition)

myworkpath = os.path.join("C:\\", "Users", "Evert Jan", "pythonprojects", "chesspython_nogithub")
myjsonsourcepath = os.path.join("C:\\", "Users", "Evert Jan", "Documents", "GitHub", "chesspython")
Test_GPPN("fide_fun")

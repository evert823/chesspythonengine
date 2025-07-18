from classes.reverse_move_finder import ReverseMoveFinder

def Test_GPPN(mypositionfilename):
    print(f"mypositionfilename {mypositionfilename}")
    myworkpath = "C:\\Users\\Evert Jan\\pythonprojects\\chesspython_nogithub"
    myjsonsourcepath = "C:\\Users\\Evert Jan\\Documents\\GitHub\\chesspython"

    rmf = ReverseMoveFinder(myworkpath, myjsonsourcepath)
    rmf.MyChessGame.LoadFromJsonFile(f"{myjsonsourcepath}\\games\\unittestgame.json", f"{myworkpath}\\positions\\{mypositionfilename}.json")
    rmf.MyChessGame.SaveAsJsonFile(f"{myworkpath}\\games_verify\\unittestgame.json", f"{myworkpath}\\positions_verify\\{mypositionfilename}.json")

    rmf.GPPN(rmf.MyChessGame.mainposition)

Test_GPPN("test_reverse_move_finder_white")
Test_GPPN("test_reverse_move_finder_black")
Test_GPPN("test_reverse_move_finder")

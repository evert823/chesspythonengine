from classes.reverse_move_finder import ReverseMoveFinder

def Test_GPPN(mypositionfilename):
    print(f"mypositionfilename {mypositionfilename}")
    myworkpath = "C:\\Users\\Evert Jan\\pythonprojects\\chesspython_nogithub"

    rmf = ReverseMoveFinder(myworkpath)
    rmf.MyChessGame.LoadFromJsonFile(".\\games\\unittestgame.json", f"{myworkpath}\\positions\\{mypositionfilename}.json")
    rmf.MyChessGame.SaveAsJsonFile(f"{myworkpath}\\games_verify\\unittestgame.json", f"{myworkpath}\\positions_verify\\{mypositionfilename}.json")

    rmf.GPPN(rmf.MyChessGame.mainposition)

Test_GPPN("test_reverse_move_finder_white")
Test_GPPN("test_reverse_move_finder_black")
Test_GPPN("test_reverse_move_finder")

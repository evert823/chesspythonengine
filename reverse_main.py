from classes.reverse_move_finder import ReverseMoveFinder

myworkpath = "C:\\Users\\Evert Jan\\pythonprojects\\chesspython_nogithub"
mypositionfilename = "test_reverse_move_finder"
n_plies = 1

rmf = ReverseMoveFinder(myworkpath)
rmf.MyChessGame.LoadFromJsonFile(".\\games\\unittestgame.json", f"{myworkpath}\\positions\\{mypositionfilename}.json")
rmf.MyChessGame.SaveAsJsonFile(f"{myworkpath}\\games_verify\\unittestgame.json", f"{myworkpath}\\positions_verify\\{mypositionfilename}.json")

myval, mymvidx, _ = rmf.MyChessGame.Calculation_n_plies(n_plies)
s = f"List : {rmf.MyChessGame.mainposition.DisplayMovelist(rmf.MyChessGame.piecetypes)}"
print(s)

try:
    mymvstr = rmf.MyChessGame.mainposition.movelist[mymvidx].ShortNotation(rmf.MyChessGame.piecetypes)
except:
    mymvstr = "No move"
print(f"Result of evaluation {n_plies} plies test_reverse_move_finder: {myval} {mymvstr}")

rmf.GPPN(rmf.MyChessGame.positionstack[0])

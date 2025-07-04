import sys
sys.path.append(".\\classes")
from chessgame import chessgame
from datetime import datetime

def Test(pchessgame, pgamefilename, ppositionfilename, n_plies):
    pchessgame.LoadFromJsonFile(".\\games\\" + pgamefilename + ".json", f"{mylocalpath}\\positions\\" + ppositionfilename + ".json")
    pchessgame.SaveAsJsonFile(f"{mylocalpath}\\games_verify\\" + pgamefilename + ".json", f"{mylocalpath}\\positions_verify\\" + ppositionfilename + ".json")
    
    pchessgame.display_when_n_plies_gt = 5
    pchessgame.presort_when_n_plies_gt = 4

    print(datetime.now())
    print(f"Running evaluation {n_plies} plies {ppositionfilename} ...")
    myval, mymvidx, _ = pchessgame.Calculation_n_plies(n_plies)
    s = f"List : {pchessgame.mainposition.DisplayMovelist(pchessgame.piecetypes)}"
    print(s)

    try:
        mymvstr = pchessgame.mainposition.movelist[mymvidx].ShortNotation(pchessgame.piecetypes)
    except:
        mymvstr = "No move"
    print(f"Result of evaluation {n_plies} plies {ppositionfilename}: {myval} {mymvstr}")
    print(datetime.now())

mylocalpath = "C:\\Users\\Evert Jan\\pythonprojects\\chesspython_nogithub"
mychessgame = chessgame(mylocalpath)

Test(mychessgame, "unittestgame", "mate_3_fide_middle", 6)

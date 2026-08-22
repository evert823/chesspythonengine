from classes.fairy_stockfish_process_handler import FairyStockfishProcessHandler
from classes.random_position_generator import RandomPositionGenerator
import os

def gen_one_from(positionfilename, max_lost_pieces_count):
    rpg.MyChessGame.LoadFromJsonFile(os.path.join(myjsonsourcepath, "games", "fairystockfishtestset.json"),
                                        os.path.join(myworkpath, "positions", f"{positionfilename}.json"))
    isvalid, message = rpg.is_valid_position(cg=rpg.MyChessGame)
    if isvalid == False:
        return (False, f"Input template invalid position {message}")

    validfound = False
    while validfound == False:
        lost_pieces_count = rpg.generate_one_position()
        isvalid, message = rpg.is_valid_position(cg=rpg.cgVerifyer)
        if isvalid == True and lost_pieces_count <= max_lost_pieces_count:
            validfound = True

    if validfound == True:
        myfen = rpg.cgVerifyer.mainposition.PositionAsFEN(ppiecetypes=rpg.MyChessGame.piecetypes)
        return (True, myfen)

myworkpath = os.path.join(os.sep, "home", "administrator", "pythonwork")
myjsonsourcepath = os.path.join(os.sep, "home", "administrator", "chesspython")
rpg = RandomPositionGenerator(myworkpath, myjsonsourcepath)

fenfilepath = os.path.join(myworkpath, "fen", "fen.txt")
fenfile = open(fenfilepath, 'w')

mypositionfilename = "template_0"
for i in range(50):
    isvalid, myfen = gen_one_from(positionfilename=mypositionfilename, max_lost_pieces_count=0)
    fenfile.write(f"{myfen}\n")

fenfile.close()

fsph = FairyStockfishProcessHandler()
#fsph.verbose = True
fsph.initial_setup()
fsph.run_positions_from_file(pfilepath=fenfilepath, depth=25)
fsph.close_engine()

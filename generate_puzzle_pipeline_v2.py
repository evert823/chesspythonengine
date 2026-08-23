from classes.fairy_stockfish_process_handler import FairyStockfishProcessHandler
from classes.random_position_generator import RandomPositionGenerator
import os
from datetime import datetime

def log(message: str):
    logfilepath = os.path.join(myworkpath, "log", "generate_v2.log")
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file2 = open(logfilepath, 'a')
    file2.write(f"{current_datetime} - {message}\n")
    file2.close()

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

def run_positions_from_file(fsph, pfilepath: str, depth: int):
    file1 = open(pfilepath, 'r', encoding='utf-8')
    Lines = file1.readlines()
    file1.close()
    for line in Lines:
        myfen = line.replace("\n", "").strip()
        mate_score = fsph.run_position(fen=myfen, depth=depth)
        s = f"fen {myfen} mate_score {mate_score}"
        print(s)
        log(message=s)

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
log(message="Finished generating positions")

fsph = FairyStockfishProcessHandler()
#fsph.verbose = True
fsph.initial_setup()
log(message=f"Calculation time per position threshold {fsph.max_sec_per_position} seconds")
log(message="Fairy-Stockfish engine setup finished and submitting 1st position now")
run_positions_from_file(fsph=fsph, pfilepath=fenfilepath, depth=25)
fsph.close_engine()

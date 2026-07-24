'''
We iteratively
- load positions
- generate predecessors
- deduplicate predecessors
- run through Fairy-Stockfish for validation
- store the positions that passed the validations

As a result we get positions with mate in n plies (half-moves)
'''

from classes.unmove_finder import UnmoveFinder
import os
from classes.fairy_stockfish_process_handler import FairyStockfishProcessHandler
import random

def create_empty_file(targetfilepath):
    tgtfile = open(targetfilepath, 'w', encoding='utf-8')
    tgtfile.close()

def append_file(fromfilepath, targetfilepath, p=1.0):
    srcfile = open(fromfilepath, 'r', encoding='utf-8')
    tgtfile = open(targetfilepath, 'a', encoding='utf-8')
    for line in srcfile:
        if random.random() < p:
            tgtfile.write(line)
    srcfile.close()
    tgtfile.close()

def deduplicate_file(fromfilepath, targetfilepath):
    seen_lines = set()
    srcfile = open(fromfilepath, 'r', encoding='utf-8')
    tgtfile = open(targetfilepath, 'w', encoding='utf-8')
    for line in srcfile:
        line2 = line.strip()
        if line2 not in seen_lines:
            seen_lines.add(line2)
            tgtfile.write(line)
    srcfile.close()
    tgtfile.close()

def write_file_0():
    umf.MyChessGame.LoadFromJsonFile(gamefilepath, initialpositionfilepath)
    myfen = umf.MyChessGame.mainposition.PositionAsFEN(umf.MyChessGame.piecetypes)
    file2 = open(os.path.join(myworkpath, "predecessorpositions", "fen_u_0_dedup_val.txt"), 'w')
    file2.write(f"{myfen}\n")
    file2.close()

def generate_predecessors_from_fen_file(i: int):
    file1 = open(os.path.join(myworkpath, "predecessorpositions", f"fen_u_{i}_dedup_val.txt"), 'r', encoding='utf-8')
    Lines = file1.readlines()
    file1.close()
    create_empty_file(targetfilepath=os.path.join(myworkpath, "predecessorpositions", f"fen_u_{i+1}.txt"))
    
    for line in Lines:
        myfen = line.replace("\n", "").strip()
        umf.MyChessGame.mainposition.PositionFromFEN(myfen, umf.MyChessGame.piecetypes)
        umf.GenerateUnmoves(pposition=umf.MyChessGame.mainposition,
                            pfilepath=os.path.join(myworkpath, "predecessorpositions", f"fen_u_{i+1}_part.txt"),
                            verbose=verbose)
        append_file(fromfilepath=os.path.join(myworkpath, "predecessorpositions", f"fen_u_{i+1}_part.txt"),
                    targetfilepath=os.path.join(myworkpath, "predecessorpositions", f"fen_u_{i+1}.txt"),
                    p=1.0)

def expected_mate_score(i):
    if i % 2 == 0:
        return (i // 2) + 1
    m = (i // 2) + 1
    return m * -1


def validate_predecessors(i: int):
    file1 = open(os.path.join(myworkpath, "predecessorpositions", f"fen_u_{i+1}_dedup.txt"), 'r', encoding='utf-8')
    Lines = file1.readlines()
    file1.close()
    file2 = open(os.path.join(myworkpath, "predecessorpositions", f"fen_u_{i+1}_dedup_val.txt"), 'w', encoding='utf-8')
    for line in Lines:
        myfen = line.replace("\n", "").strip()
        mate_score = fsph.run_position(fen=myfen, depth=20)
        if verbose == True:
            print(f"fen {myfen} mate_score {mate_score}")
        if mate_score == expected_mate_score(i):
            file2.write(myfen + "\n")
    file2.close()

ENGINE_PATH = "/home/administrator/Fairy-Stockfish/src/stockfish-largeboards"
INI_PATH = "/home/administrator/stockfish_use/variant_inifiles/guardendgame.ini"
verbose = False

myworkpath = os.path.join(os.sep, "home", "administrator", "pythonwork")
myjsonsourcepath = os.path.join(os.sep, "home", "administrator", "chesspython")
gamefilepath = os.path.join(myjsonsourcepath, "games", "guardendgame.json")
initialpositionfilepath = os.path.join(myworkpath, "positions", "crazymate.json")

fsph = FairyStockfishProcessHandler()
fsph.initial_setup()

umf = UnmoveFinder(myworkpath, myjsonsourcepath)
write_file_0()

for i in range(5):
    print(f"generate puzzles iteration {i} started")
    generate_predecessors_from_fen_file(i=i)
    deduplicate_file(fromfilepath=os.path.join(myworkpath, "predecessorpositions", f"fen_u_{i+1}.txt"),
                    targetfilepath=os.path.join(myworkpath, "predecessorpositions", f"fen_u_{i+1}_dedup.txt"))
    print(f"generate puzzles iteration {i} now running Fairy-Stockfish process")
    validate_predecessors(i=i)
    print(f"generate puzzles iteration {i} ended")



fsph.close_engine()

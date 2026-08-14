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
from datetime import datetime

def log(message: str):
    logfilepath = os.path.join(myworkpath, "log", "generate.log")
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file2 = open(logfilepath, 'a')
    file2.write(f"{current_datetime} - {message}\n")
    file2.close()

def create_empty_file(targetfilepath):
    tgtfile = open(targetfilepath, 'w', encoding='utf-8')
    tgtfile.close()

def append_file(fromfilepath, targetfilepath):
    srcfile = open(fromfilepath, 'r', encoding='utf-8')
    tgtfile = open(targetfilepath, 'a', encoding='utf-8')
    for line in srcfile:
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

def random_shrink_file(fromfilepath, targetfilepath):
    '''
    if srcfile has <= max_appr_result_iteration rows, write all rows
    if srcfile has > max_appr_result_iteration rows, then
    write random subset of approximately max_appr_result_iteration
    '''
    srcfile = open(fromfilepath, 'r', encoding='utf-8')
    tgtfile = open(targetfilepath, 'w', encoding='utf-8')
    Lines = srcfile.readlines()
    line_count = len(Lines)
    lines_written = 0
    if line_count == 0:
        p = 1.0
    elif line_count <= max_appr_result_iteration:
        p = 1.0
    else:
        p = max_appr_result_iteration / line_count
    for lnr in range(line_count):
        line = Lines[lnr]
        ev = random.random()
        if ev <= p:
            lines_written += 1
            tgtfile.write(line)
    srcfile.close()
    tgtfile.close()
    log(f"random_shrink {fromfilepath} {line_count} {targetfilepath} {lines_written}")

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
    
    for lnr in range(len(Lines)):
        myfen = Lines[lnr].replace("\n", "").strip()
        if lnr % 20 == 0:
            log(f"{lnr} fen {myfen} generating the unmoves")
        umf.MyChessGame.mainposition.PositionFromFEN(myfen, umf.MyChessGame.piecetypes)
        umf.GenerateUnmoves(pposition=umf.MyChessGame.mainposition,
                            pfilepath=os.path.join(myworkpath, "predecessorpositions", f"fen_u_{i+1}_part.txt"),
                            verbose=verbose)
        append_file(fromfilepath=os.path.join(myworkpath, "predecessorpositions", f"fen_u_{i+1}_part.txt"),
                    targetfilepath=os.path.join(myworkpath, "predecessorpositions", f"fen_u_{i+1}.txt"))

def expected_mate_score(i):
    if i % 2 == 0:
        return (i // 2) + 1
    m = (i // 2) + 1
    return m * -1

def depth_from_iteration(i):
    return ( (7 * (i + 1)) // 2 ) + 10

def validate_predecessors(i: int):
    mydepth = depth_from_iteration(i)
    log(f"Fairy-Stockfish depth {mydepth}")
    fsph.initial_setup()
    file1 = open(os.path.join(myworkpath, "predecessorpositions", f"fen_u_{i+1}_dedup_sized.txt"), 'r', encoding='utf-8')
    Lines = file1.readlines()
    file1.close()
    file2 = open(os.path.join(myworkpath, "predecessorpositions", f"fen_u_{i+1}_dedup_val.txt"), 'w', encoding='utf-8')
    my_expected_mate_score = expected_mate_score(i)
    for lnr in range(len(Lines)):
        myfen = Lines[lnr].replace("\n", "").strip()
        mate_score = fsph.run_position(fen=myfen, depth=mydepth)
        if lnr % 20 == 0:
            log(f"{lnr} fen {myfen} mate_score {mate_score} expecting {my_expected_mate_score}")
        if my_expected_mate_score > 0 and mate_score > 3:
            log(f"{lnr} fen {myfen} mate_score {mate_score} expecting {my_expected_mate_score} byproduct")
        if verbose == True:
            print(f"fen {myfen} mate_score {mate_score}")
        if mate_score == my_expected_mate_score:
            file2.write(myfen + "\n")
    file2.close()
    fsph.close_engine()

def PiecelistForUncapture_from_iteration(i):
    if i == 0:
        return ["Rook", "Guard"]
    if i == 1:
        return ["Rook", "Guard"]
    if i == 2:
        return ["Rook", "Guard"]
    if i == 3:
        return ["Rook", "Guard"]
    return []

verbose = False
max_appr_result_iteration = 500

myworkpath = os.path.join(os.sep, "home", "administrator", "pythonwork")
myjsonsourcepath = os.path.join(os.sep, "home", "administrator", "chesspython")
gamefilepath = os.path.join(myjsonsourcepath, "games", "fairystockfishtestset.json")
initialpositionfilepath = os.path.join(myworkpath, "positions", "puzzlechallenge.json")

fsph = FairyStockfishProcessHandler()

umf = UnmoveFinder(myworkpath, myjsonsourcepath)
write_file_0()

for i in range(7):
    log(f"generate puzzles iteration {i} started")
    umf.PiecelistForUncapture = PiecelistForUncapture_from_iteration(i)
    generate_predecessors_from_fen_file(i=i)
    log(f"deduplication {i} started")
    deduplicate_file(fromfilepath=os.path.join(myworkpath, "predecessorpositions", f"fen_u_{i+1}.txt"),
                    targetfilepath=os.path.join(myworkpath, "predecessorpositions", f"fen_u_{i+1}_dedup.txt"))
    random_shrink_file(fromfilepath=os.path.join(myworkpath, "predecessorpositions", f"fen_u_{i+1}_dedup.txt"),
                    targetfilepath=os.path.join(myworkpath, "predecessorpositions", f"fen_u_{i+1}_dedup_sized.txt"))
    log(f"generate puzzles iteration {i} now starting Fairy-Stockfish process")
    validate_predecessors(i=i)
    log(f"generate puzzles iteration {i} ended")

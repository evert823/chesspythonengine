import os
from classes.fairy_stockfish_process_handler import FairyStockfishProcessHandler
from datetime import datetime

def log(message: str):
    logfilepath = os.path.join(myworkpath, "log", "testrun.log")
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file2 = open(logfilepath, 'a')
    file2.write(f"{current_datetime} - {message}\n")
    file2.close()

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
fenfilepath = os.path.join(myworkpath, "fen", "fen.txt")

fsph = FairyStockfishProcessHandler()
fsph.verbose = True
fsph.initial_setup()

#mate_score = fsph.run_position(fen="k6nr1/p2m6/pP8/2P7/2Np6/1KP7/C9/R9 w", depth=25)
#print(f"mate_score seen by fsph {mate_score}")

run_positions_from_file(fsph=fsph, pfilepath=fenfilepath, depth=25)

fsph.close_engine()

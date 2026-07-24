import subprocess
import re

ENGINE_PATH = "/home/administrator/Fairy-Stockfish/src/stockfish-largeboards"
INI_PATH = "/home/administrator/stockfish_use/variant_inifiles/guardendgame.ini"
verbose = False

def create_process():
    engine = subprocess.Popen(
        [ENGINE_PATH],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    return engine


def send(engine, cmd):
    engine.stdin.write(cmd + "\n")
    engine.stdin.flush()

def init_uci(engine):
    send(engine=engine, cmd="uci")
    while True:
        line = engine.stdout.readline().strip()
        if line == "uciok":
            print(line)
            break

def verify_uci(engine):
    send(engine=engine, cmd="isready")
    while True:
        line = engine.stdout.readline().strip()
        if line == "readyok":
            print(line)
            break

def load_variant(engine):
    send(engine=engine, cmd=f"load {INI_PATH}")

def setvariant_uci(engine):
    send(engine=engine, cmd="setoption name UCI_Variant value Guardendgame")


def detect_fsf_mate_score(line):
    '''
    FSF displays "score mate 2" if mate in 2
    FSF displays "score mate -2" if mate in 2 and losing army to move (1 ply further away from mate)
    '''
    m = re.search(r"\bscore mate\s+(-?\d+)\b", line)
    if m is not None:
        mate_score = int(m.group(1))
        return mate_score
    return None

def run_position(engine, fen: str, depth: int):
    mate_score = None

    send(engine=engine, cmd="setoption name Clear Hash")
    #Because if we don't then FSF becomes inpredictable

    send(engine=engine, cmd=f"position fen {fen}")
    send(engine=engine, cmd=f"go depth {str(depth)}")
    while True:
        line = engine.stdout.readline().strip()
        if verbose == True:
            print(line)
        if line.startswith("info depth") and line.find(" score ") > -1:
            mate_score = detect_fsf_mate_score(line)
        if line.startswith("bestmove"):
            break
    return mate_score

def verify_fsf_behaviour(engine):
    print("verify_fsf_behaviour started ...")
    fenlist = ["7k2/10/6K3/10/10/10/3R6/10 w",
               "6k3/10/6K3/10/10/10/3R6/10 b",
               "2R5/3P4/1b2p3/2qNRp2/2kPnr1p/pgPqKGrP/Bp1QP1P1/8 w",
               "8/1k6/8/1BK5/3N4/8/8/8 w",
               "10/1k2G5/10/2K7/3N6/10/10/10 w",
               "10/2k2G4/10/2K7/3N6/10/10/10 w"]
    depthlist = [8, 8, 4, 40, 40, 40]
    expectedmatescorelist = [2, -2, 1, 7, 5, 6]

    for i in range(6):
        mate_score = run_position(engine=engine, fen=fenlist[i], depth=depthlist[i])
        if mate_score is None:
            raise Exception("FSF setup not OK")
        elif mate_score != expectedmatescorelist[i]:
            raise Exception("FSF setup not OK")
    print("verify_fsf_behaviour OK")

def run_positions_from_file(engine, pfilepath: str, depth: int):
    file1 = open(pfilepath, 'r', encoding='utf-8')
    Lines = file1.readlines()
    file1.close()
    for line in Lines:
        myfen = line.replace("\n", "").strip()
        mate_score = run_position(engine=engine, fen=myfen, depth=depth)
        if verbose == True:
            print(f"fen {myfen} mate_score {mate_score}")

engine = create_process()
init_uci(engine=engine)
verify_uci(engine=engine)
load_variant(engine=engine)
setvariant_uci(engine=engine)
verify_fsf_behaviour(engine=engine)

#the output of unmove_finder_main.py
mate_score = run_positions_from_file(engine=engine,
                                     pfilepath="/home/administrator/pythonwork/predecessorpositions/fen.txt",
                                     depth=5)

send(engine=engine, cmd="quit")
engine.wait()

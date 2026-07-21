import subprocess

ENGINE_PATH = "/home/administrator/Fairy-Stockfish/src/stockfish-largeboards"
INI_PATH = "/home/administrator/stockfish_use/variant_inifiles/guardendgame.ini"

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


def run_position(engine, fen: str, depth: int):
    send(engine=engine, cmd=f"position fen {fen}")
    send(engine=engine, cmd=f"go depth {str(depth)}")
    while True:
        line = engine.stdout.readline().strip()
        if line.startswith("info depth") and line.find(" score ") > -1:
            print(line)
        if line.startswith("bestmove"):
            print(fen, "->", line)
            break

engine = create_process()
init_uci(engine=engine)
verify_uci(engine=engine)
load_variant(engine=engine)
setvariant_uci(engine=engine)

#crazy mate in 1
run_position(engine=engine, fen="2R5/3P4/1b2p3/2qNRp2/2kPnr1p/pgPqKGrP/Bp1QP1P1/8 w", depth=4)

#objective mate in 7 stabilizes depth 31
run_position(engine=engine, fen="8/1k6/8/1BK5/3N4/8/8/8 w", depth=40)

#objective mate in 5 stabilizes depth 9
run_position(engine=engine, fen="10/1k2G5/10/2K7/3N6/10/10/10 w", depth=40)

#objective mate 6 stabilizes depth 16
run_position(engine=engine, fen="10/2k2G4/10/2K7/3N6/10/10/10 w", depth=40)

send(engine=engine, cmd="quit")
engine.wait()

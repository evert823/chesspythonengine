import subprocess

def create_process():
    engine = subprocess.Popen(
        [
            "/home/administrator/Fairy-Stockfish/src/stockfish-largeboards"
        ],
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
    send(engine=engine, cmd=f"load /home/administrator/stockfish_use/variant_inifiles/guardendgame.ini")

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
run_position(engine=engine, fen="2R5/3P4/1b2p3/2qNRp2/2kPnr1p/pgPqKGrP/Bp1QP1P1/8 w", depth=4)

send(engine=engine, cmd="quit")
engine.wait()

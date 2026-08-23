import subprocess
import re
import time
from datetime import datetime

ENGINE_PATH = "/home/administrator/Fairy-Stockfish/src/stockfish-largeboards"
INI_PATH = "/home/administrator/stockfish_use/variant_inifiles/fairystockfishtestset.ini"
VARIANT_NAME = "FairyStockfishTestset"

class FairyStockfishProcessHandler:
    def __init__(self):
        self.verbose = False
        self.max_sec_per_position = 180.0
        self.engine = None

    def create_process(self):
        self.engine = subprocess.Popen(
            [ENGINE_PATH],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

    def send(self, cmd):
        self.engine.stdin.write(cmd + "\n")
        self.engine.stdin.flush()

    def init_uci(self):
        self.send(cmd="uci")
        while True:
            line = self.engine.stdout.readline().strip()
            if line == "uciok":
                print(line)
                break

    def verify_uci(self):
        self.send(cmd="isready")
        while True:
            line = self.engine.stdout.readline().strip()
            if line == "readyok":
                print(line)
                break

    def load_variant(self):
        print(f"Loading variant.ini {INI_PATH}")
        self.send(cmd=f"load {INI_PATH}")

    def setvariant_uci(self):
        self.send(cmd=f"setoption name UCI_Variant value {VARIANT_NAME}")

    def detect_fsf_mate_score(self, line):
        '''
        FSF displays "score mate 2" if mate in 2
        FSF displays "score mate -2" if mate in 2 and losing army to move (1 ply further away from mate)
        '''
        m = re.search(r"\bscore mate\s+(-?\d+)\b", line)
        if m is not None:
            mate_score = int(m.group(1))
            return mate_score
        return None

    def initial_setup(self):
        self.create_process()
        self.init_uci()
        self.verify_uci()
        self.load_variant()
        self.setvariant_uci()
        self.verify_fsf_behaviour()

    def close_engine(self):
        self.send(cmd="quit")
        self.engine.wait()
        time.sleep(5)

    def run_position(self, fen: str, depth: int):
        mate_score = None

        self.send(cmd="setoption name Clear Hash")
        #Because if we don't then FSF becomes inpredictable

        #The wall is hardcoded asterisk for Fairy-Stockfish while we use letter x or X
        fen2 = fen.replace("x", "*")
        fen2 = fen2.replace("X", "*")

        self.send(cmd=f"position fen {fen2}")
        movetime_ms = int(self.max_sec_per_position * 1000)
        self.send(cmd=f"go depth {str(depth)} movetime {movetime_ms}")
        while True:
            line = self.engine.stdout.readline().strip()
            if self.verbose == True:
                print(line)
            if line.startswith("info depth") and line.find(" score ") > -1:
                mate_score = self.detect_fsf_mate_score(line)
            if line.startswith("bestmove"):
                break
        return mate_score

    def verify_fsf_behaviour(self):
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
            mate_score = self.run_position(fen=fenlist[i], depth=depthlist[i])
            if mate_score is None:
                raise Exception("FSF setup not OK")
            elif mate_score != expectedmatescorelist[i]:
                raise Exception("FSF setup not OK")
        print("verify_fsf_behaviour OK")


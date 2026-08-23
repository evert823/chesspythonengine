from classes.fairy_stockfish_process_handler import FairyStockfishProcessHandler

fsph = FairyStockfishProcessHandler()
fsph.verbose = True
fsph.initial_setup()

mate_score = fsph.run_position(fen="k6nr1/p2m6/pP8/2P7/2Np6/1KP7/C9/R9 w", depth=25)
print(f"mate_score seen by fsph {mate_score}")
fsph.close_engine()

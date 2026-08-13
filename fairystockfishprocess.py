from classes.fairy_stockfish_process_handler import FairyStockfishProcessHandler

fsph = FairyStockfishProcessHandler()
fsph.verbose = True
fsph.initial_setup()

#the output of unmove_finder_main.py
fsph.run_positions_from_file(pfilepath="/home/administrator/pythonwork/predecessorpositions/fen.txt",
                             depth=50)
fsph.close_engine()

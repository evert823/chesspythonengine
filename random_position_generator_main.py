from classes.random_position_generator import RandomPositionGenerator
import os

def load_template(positionfilename):
    rpg.MyChessGame.LoadFromJsonFile(os.path.join(myjsonsourcepath, "games", "fairystockfishtestset.json"),
                                        os.path.join(myworkpath, "positions", f"{positionfilename}.json"))
    rpg.MyChessGame.SaveAsJsonFile(os.path.join(myworkpath, "games_verify", "fairystockfishtestset.json"),
                                    os.path.join(myworkpath, "positions_verify", f"{positionfilename}.json"))
    rpg.is_valid_position(cg=rpg.MyChessGame)

    lost_pieces_count = rpg.generate_one_position()
    print(f"lost_pieces_count {lost_pieces_count}")
    rpg.cgVerifyer.SaveAsJsonFile(os.path.join(myworkpath, "games_verify", "fairystockfishtestset.json"),
                                    os.path.join(myworkpath, "randompositions", f"from_{positionfilename}.json"))
    rpg.is_valid_position(cg=rpg.cgVerifyer)

#myworkpath = os.path.join(os.sep, "home", "administrator", "pythonwork")
#myjsonsourcepath = os.path.join(os.sep, "home", "administrator", "chesspython")
myworkpath = os.path.join("C:\\", "Users", "Evert Jan", "pythonprojects", "chesspython_nogithub")
myjsonsourcepath = os.path.join("C:\\", "Users", "Evert Jan", "Documents", "GitHub", "chesspython")
rpg = RandomPositionGenerator(myworkpath, myjsonsourcepath)
#mypositionfilename = "template_0"
mypositionfilename = "mate_in_4_for_white_hard_chesscom"
load_template(positionfilename=mypositionfilename)

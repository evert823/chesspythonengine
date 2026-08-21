from classes.random_position_generator import RandomPositionGenerator
import os

def test_is_valid(positionfilename):
    rpg.MyChessGame.LoadFromJsonFile(os.path.join(myjsonsourcepath, "games", "fairystockfishtestset.json"),
                                        os.path.join(myworkpath, "positions", f"{positionfilename}.json"))
    rpg.MyChessGame.SaveAsJsonFile(os.path.join(myworkpath, "games_verify", "fairystockfishtestset.json"),
                                    os.path.join(myworkpath, "positions_verify", f"{positionfilename}.json"))
    isvalid, message = rpg.is_valid_position(cg=rpg.MyChessGame)
    print(f"isvalid {isvalid} message {message}")

def test_is_valid_all():
    test_is_valid(positionfilename="invalid1")
    test_is_valid(positionfilename="invalid2")
    test_is_valid(positionfilename="invalid3")
    test_is_valid(positionfilename="invalid4")
    test_is_valid(positionfilename="invalid5")
    test_is_valid(positionfilename="isalreadymate_white")
    test_is_valid(positionfilename="isalreadymate_black")
    test_is_valid(positionfilename="isalreadystalemate_white")
    test_is_valid(positionfilename="isalreadystalemate_black")

def gen_one_from(positionfilename, max_lost_pieces_count):
    rpg.MyChessGame.LoadFromJsonFile(os.path.join(myjsonsourcepath, "games", "fairystockfishtestset.json"),
                                        os.path.join(myworkpath, "positions", f"{positionfilename}.json"))
    isvalid, message = rpg.is_valid_position(cg=rpg.MyChessGame)
    if isvalid == False:
        return (False, f"Input template invalid position {message}")

    validfound = False
    while validfound == False:
        lost_pieces_count = rpg.generate_one_position()
        isvalid, message = rpg.is_valid_position(cg=rpg.cgVerifyer)
        if isvalid == True and lost_pieces_count <= max_lost_pieces_count:
            validfound = True

    if validfound == True:
        myfen = rpg.cgVerifyer.mainposition.PositionAsFEN(ppiecetypes=rpg.MyChessGame.piecetypes)
        return (True, myfen)

#myworkpath = os.path.join(os.sep, "home", "administrator", "pythonwork")
#myjsonsourcepath = os.path.join(os.sep, "home", "administrator", "chesspython")
myworkpath = os.path.join("C:\\", "Users", "Evert Jan", "pythonprojects", "chesspython_nogithub")
myjsonsourcepath = os.path.join("C:\\", "Users", "Evert Jan", "Documents", "GitHub", "chesspython")
rpg = RandomPositionGenerator(myworkpath, myjsonsourcepath)

#test_is_valid_all()

mypositionfilename = "template_0"
for i in range(50):
    isvalid, myfen = gen_one_from(positionfilename=mypositionfilename, max_lost_pieces_count=0)
    print(f"isvalid {isvalid} myfen {myfen}")

import json
import sys
from draw import draw
from place import place


def eprint(*args, **kwargs):
    """Prints to stderr."""
    print(*args, file=sys.stderr, **kwargs)


def beginReadLine():
    while True:
        console_input = input()
        try:
            data = json.loads(console_input)
            match data["state"].get("message"):
                case "NEWGAME" | "ENDGAME":
                    startEndGame(data)
                case None:
                    randomIsh(data)
        except json.JSONDecodeError as e:
            eprint(f"Invalid JSON: {e}")
        # except Exception as e:
        #     eprint(f"Exception: {e}")


def startEndGame(data: dict):
    output = {"move": 0, "messageID": data["messageID"]}
    print(json.dumps(output))


def randomIsh(data: dict):
    if not data["state"]["activeTurn"]:
        output = {"move": "RANDOM", "messageID": data["messageID"]}
        print(json.dumps(output))
    else:
        match data["state"]["subTurn"]:
            case 0 | 1:
                draw(data)
            case 2:
                place(data)
            case _:
                output = {"move": "RANDOM", "messageID": data["messageID"]}
                print(json.dumps(output))

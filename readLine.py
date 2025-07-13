import json
import sys
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


def startEndGame(data: dict):
    output = {"move": 0, "messageID": data["messageID"]}
    print(json.dumps(output))


def randomIsh(data: dict):
    match data["state"]["subTurn"]:
        case 2:
            place(data)
        case _:
            output = {"move": "RANDOM", "messageID": data["messageID"]}
            print(json.dumps(output))

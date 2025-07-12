import json
import sys


def eprint(*args, **kwargs):
    """Prints to stderr."""
    print(*args, file=sys.stderr, **kwargs)


def beginReadLine():
    while True:
        console_input = input()
        try:
            data = json.loads(console_input)
            eprint(data)
            match data["state"].get("message"):
                case "NEWGAME" | "ENDGAME":
                    startEndGame(data)
                case None:
                    random(data)
        except json.JSONDecodeError as e:
            eprint(f"Invalid JSON: {e}")


def startEndGame(data: dict[str, str]):
    eprint("Startgame Recieved")
    output = {"move": 0, "messageID": data["messageID"]}
    print(json.dumps(output))


def endGame(data: dict[str, str]):
    pass


def random(data: dict[str, str]):
    output = {"move": "RANDOM", "messageID": data["messageID"]}
    print(json.dumps(output))

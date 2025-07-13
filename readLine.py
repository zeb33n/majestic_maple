import json
import sys
from place import place, get_best_play
from discard import get_discard_card


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
        except Exception as e:
            eprint(f"Exception: {e}")


def startEndGame(data: dict):
    output = {"move": 0, "messageID": data["messageID"]}
    print(json.dumps(output))


def discard(data: dict):
    """
    Handles discard phase (subTurn 3) using our discard heuristic.
    
    Args:
        data: Game data with messageID and state (same format as place())
    """
    try:
        # Check if we have cached card scores from placement phase
        from place import cached_card_scores
        if not cached_card_scores:
            # Cache not populated, need to run placement analysis first
            eprint("Cache empty, running placement analysis for discard decision")
            get_best_play(data["state"])
        
        # Get discard recommendation using our heuristic
        discard_card = get_discard_card(data["state"])
        
        # Format response for game engine
        output = {
            "move": discard_card,
            "messageID": data["messageID"]
        }
        print(json.dumps(output))
        
    except Exception as e:
        eprint(f"Error in discard logic: {e}")
        # Fallback to random discard
        output = {"move": "RANDOM", "messageID": data["messageID"]}
        print(json.dumps(output))


def randomIsh(data: dict):
    match data["state"]["subTurn"]:
        case 2:
            place(data)
        case 3:
            discard(data)
        case _:
            output = {"move": "RANDOM", "messageID": data["messageID"]}
            print(json.dumps(output))

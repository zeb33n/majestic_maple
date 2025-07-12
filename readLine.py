import json
import sys
from scoring import PlayArea, get_weighted_scores
from copy import deepcopy


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
            playarea = data["state"]["playArea"]
            plays = _get_valid_play_coordinates(data["state"]["playArea"])
            best_score = 0
            for play in plays:
                for card in data["state"]["hand"]:
                    pa = deepcopy(playarea)
                    pa[play[0]][play[1]] = card
                    weighted_scores = get_weighted_scores(pa)
                    score = sum(weighted_scores.values())
                    if score > best_score:
                        best_score = score
                        best_play = (card, play)

            output = {
                "move": {"card": best_play[0], "coord": best_play[1]},
                "messageID": data["messageID"],
            }
            print(json.dumps(output))

        case _:
            output = {"move": "RANDOM", "messageID": data["messageID"]}
            print(json.dumps(output))


def _get_valid_play_coordinates(play_area: dict) -> set[tuple[int, int]]:
    """
    Calculates all valid empty coordinates adjacent to existing cards.
    """
    # If the play area is empty, the only valid move is at (0, 0).
    if not play_area:
        return {(0, 0)}

    occupied_coords = set()
    empty_adjacent_coords = set()

    # First, find all currently occupied coordinates.
    # The keys in the JSON are strings, so they must be cast to integers.
    for x_str, row in play_area.items():
        for y_str in row.keys():
            occupied_coords.add((int(x_str), int(y_str)))

    # Now, find all empty spaces adjacent to the occupied ones.
    for x, y in occupied_coords:
        # Check the four adjacent positions (up, down, left, right)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            adj_coord = (x + dx, y + dy)
            if adj_coord not in occupied_coords:
                empty_adjacent_coords.add(adj_coord)

    return empty_adjacent_coords

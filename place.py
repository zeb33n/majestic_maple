from copy import deepcopy
from scoring import get_weighted_scores
from utils import get_valid_play_coordinates
import json
import sys


def eprint(*args, **kwargs):
    """Prints to stderr."""
    print(*args, file=sys.stderr, **kwargs)


def assess_card_placement(
    card: tuple[str, int], coord: tuple[int, int], state: dict
) -> float:
    state_copy = deepcopy(state)
    x_key = str(coord[0])
    y_key = str(coord[1])
    a = state_copy["playArea"].get(x_key)
    if a is not None:
        state_copy["playArea"][x_key][y_key] = card
    else:
        state_copy["playArea"][x_key] = {y_key: card}

    weighted_scores = get_weighted_scores(state_copy)
    return sum(weighted_scores.values())


def get_best_play(state: dict) -> tuple[tuple[str, int], tuple[int, int]]:
    coords = get_valid_play_coordinates(state["playArea"])
    best_score = 0
    best_play = (state["hand"][0], list(coords)[0])
    for card in state["hand"]:
        for coord in coords:
            score = assess_card_placement(card, coord, state)
            if score > best_score:
                best_score = score
                best_play = (card, coord)

    return best_play


def place(data: dict):
    if not data["state"]["activeTurn"]:
        output = {"move": "RANDOM", "messageID": data["messageID"]}
        print(json.dumps(output))
    else:
        card, coord = get_best_play(data["state"])
        output = {
            "move": {"card": card, "coord": coord},
            "messageID": data["messageID"],
        }
        print(json.dumps(output))


if __name__ == "__main__":
    test_state = {
        "deck": 2,
        "hand": [["R", 1], ["J", 3], ["R", 4], ["J", 5], ["O", 4], ["J", 4], ["R", 3]],
        "discard": [],
        "opponentDiscard": [["C", 5], ["R", 5]],
        "playArea": {
            "0": {"0": ["W", 2], "1": ["C", 6], "2": ["R", 7], "-1": ["M", 8]},
            "1": {"0": ["O", 6], "1": ["M", 4], "2": ["O", 1], "-1": ["O", 5]},
            "2": {"0": ["J", 2], "1": ["J", 6], "-1": ["M", 2]},
            "-1": {"0": ["R", 6], "1": ["C", 4], "-1": ["C", 3]},
            "-2": {"1": ["C", 2]},
        },
        "opponentPlayArea": {
            "0": {"0": ["W", 8], "-1": ["R", 2]},
            "1": {"0": ["O", 2]},
            "-1": {"0": ["M", 6], "1": ["O", 8], "2": ["M", 7]},
            "-2": {"0": ["W", 6], "1": ["W", 4], "2": ["J", 7], "-1": ["J", 8]},
            "-3": {
                "0": ["M", 3],
                "1": ["W", 7],
                "2": ["M", 5],
                "-1": ["C", 7],
                "-2": ["W", 3],
            },
        },
        "opponentHand": [None, ["W", 5], ["R", 8], None, None, ["C", 1], ["C", 8]],
        "turn": 30,
        "subTurn": 0,
        "previousTurn": {"move": ["R", 5], "metaData": False},
    }
    get_best_play(test_state)

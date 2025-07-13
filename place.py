from copy import deepcopy
from scoring import get_weighted_scores
from utils import get_valid_play_coordinates
import json


def assess_card_placement(
    card: tuple[str, int], coord: tuple[int, int], state: dict
) -> float:
    state = deepcopy(state)
    a = state["playArea"].get(coord[0])
    if a is not None:
        state["playArea"][coord[0]][coord[1]] = card
    else:
        state["playArea"][coord[0]] = {coord[1]: card}

    weighted_scores = get_weighted_scores(state)
    return sum(weighted_scores.values())


def get_best_play(state: dict) -> tuple[tuple[str, int], tuple[int, int]]:
    plays = get_valid_play_coordinates(state["playArea"])
    best_score = 0
    best_play = (state["hand"][0], list(plays)[0])
    for play in plays:
        for card in state["hand"]:
            score = assess_card_placement(card, play, state)
            if score > best_score:
                best_score = score
                best_play = (card, play)

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

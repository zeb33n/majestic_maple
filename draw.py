from utils import get_valid_play_coordinates, assess_card_placement, sample_cards
from scoring import ALL_CARDS
import json
import sys
import magic


def assess_draw(state: dict) -> int:

    # eprint(f'discard: {state["discard"]}')
    # eprint(f'op: {state["opponentDiscard"]}')

    coords = get_valid_play_coordinates(state["playArea"])
    discard_scores = {
        pile: assess_card(state[pile].pop(), coords, state)
        for pile in ["discard", "opponentDiscard"]
        if len(state[pile]) > 0
    }
    seen_cards = (
        state["hand"]
        + state["opponentHand"]
        + state["discard"]
        + state["opponentDiscard"]
        + list(y for x in state["playArea"].values() for y in x.values())
        + list(y for x in state["opponentPlayArea"].values() for y in x.values())
    )
    unknown_cards = ALL_CARDS - {tuple(card) for card in seen_cards if not card is None}
    lim_calcs = magic.DRAW_LIM_CALCS
    unknown_cards = sample_cards(unknown_cards, int(lim_calcs / len(coords)))
    unknown_card_scores = [assess_card(card, coords, state) for card in unknown_cards]
    avg = sum(unknown_card_scores) / len(unknown_card_scores)
    discard_scores.update({"deck": avg * (1 / len(unknown_card_scores))})

    return {"deck": 0, "discard": 1, "opponentDiscard": 2}[
        max(discard_scores, key=discard_scores.get)
    ]


def assess_card(
    card: tuple[str, int], coords: set[tuple[int, int]], state: dict
) -> float:
    return max([assess_card_placement(card, coord, state) for coord in coords])


def eprint(*args, **kwargs):
    """Prints to stderr."""
    print(*args, file=sys.stderr, **kwargs)


def draw(data: dict):
    choice = assess_draw(data["state"])
    output = {
        "move": choice,
        "messageID": data["messageID"],
    }
    # eprint(json.dumps(output))
    print(json.dumps(output))

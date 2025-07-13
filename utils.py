from copy import deepcopy
from scoring import get_weighted_scores
import random


def sample_cards(cards: set, N) -> set:
    if N > len(cards):
        return cards
    return set(random.sample(list(cards), N))


def get_valid_play_coordinates(play_area: dict) -> set[tuple[int, int]]:
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

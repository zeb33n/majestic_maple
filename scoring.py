from typing import Dict, List, Tuple
from itertools import combinations
import math

# Type hints for better readability
Species = str
Rank = int
Card = Tuple[Species, Rank]
Coord = Tuple[int, int]
PlayArea = Dict[str, Dict[str, Card]]
Path = List[Card]

ALL_CARDS = set(
    [
        (species, num)
        for species in ["J", "R", "C", "M", "O", "W"]
        for num in range(1, 9)
    ]
)


def card_string(card: Card) -> str:
    """Creates a unique string for a card tuple, e.g., ('W', 8) -> 'W8'."""
    return f"{card[0]}{card[1]}"


def score_path(path: Path, species: Species) -> int:
    """Calculates the score for a single, valid path."""
    if len(path) <= 1:
        return 0

    first_card = path[0]
    last_card = path[-1]

    # A path only scores if the first and last cards match the species being scored.
    if first_card[0] != species or last_card[0] != species:
        return 0

    score = len(path)

    # Bonus: +1 point per card if the path is >= 4 cards and all of the same species.
    is_monospecies_path = all(card[0] == species for card in path)
    if is_monospecies_path and len(path) >= 4:
        score += len(path)

    # Bonus: +1 point for a path starting with a 1.
    if first_card[1] == 1:
        score += 1

    # Bonus: +2 points for a path ending with an 8.
    if last_card[1] == 8:
        score += 2

    return score


def get_score_from_starting_card(
    play_area: PlayArea, start_coord: Coord, species: Species
) -> int:
    """
    Performs a Depth-First Search (DFS) to find the highest scoring path
    originating from a given starting coordinate.
    """
    # The stack holds dictionaries representing the state of each search branch
    search_track_stack = [{"path": [], "coord": start_coord, "visited_cards": set()}]
    highest_score = 0

    while search_track_stack:
        current_track = search_track_stack.pop()
        path = current_track["path"]
        coord = current_track["coord"]
        visited_cards = current_track["visited_cards"]

        x_str, y_str = str(coord[0]), str(coord[1])
        card = play_area.get(x_str, {}).get(y_str)

        # This should not happen if called correctly, but is a safe guard.
        if not card:
            continue

        # Add the current card to the path and the visited set for this search branch
        new_path = path + [card]
        new_visited_cards = visited_cards.copy()
        new_visited_cards.add(card_string(card))

        # Calculate and update the highest score found so far
        current_score = score_path(new_path, species)
        if current_score > highest_score:
            highest_score = current_score

        # Explore adjacent neighbors to extend the path
        x, y = coord
        # [(Up), (Down), (Right), (Left)]
        coord_options = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]

        for next_x, next_y in coord_options:
            next_x_str, next_y_str = str(next_x), str(next_y)
            next_card = play_area.get(next_x_str, {}).get(next_y_str)

            # A card is a valid next step in a path if:
            # 1. It exists.
            # 2. It has not been visited in this specific path already.
            # 3. Its rank is strictly greater than the current card's rank.
            if (
                next_card
                and card_string(next_card) not in new_visited_cards
                and next_card[1] > card[1]
            ):

                # Add the next state to the search stack
                search_track_stack.append(
                    {
                        "path": new_path,
                        "coord": (next_x, next_y),
                        "visited_cards": new_visited_cards,
                    }
                )

    return highest_score


def get_all_cards_of_species(
    play_area: PlayArea, species: Species
) -> List[Tuple[Coord, Card]]:
    """Finds all cards of a given species in the play area."""
    cards_of_species = []
    for x_str, row in play_area.items():
        for y_str, card in row.items():
            if card[0] == species:
                # Convert string keys back to integers for coordinate calculations
                coord = (int(x_str), int(y_str))
                cards_of_species.append((coord, card))
    return cards_of_species


def score_play_area(play_area: PlayArea, species: Species) -> int:
    """
    Calculates the total score for a given species by checking all possible
    starting cards of that species.
    """
    highest_score = 0
    starting_cards = get_all_cards_of_species(play_area, species)

    # Each card of the target species is a potential start of a scoring path.
    for coord, _ in starting_cards:
        score = get_score_from_starting_card(play_area, coord, species)
        if score > highest_score:
            highest_score = score

    return highest_score


def calculate_all_scores(play_area: PlayArea) -> Dict[Species, int]:
    """
    The main function to calculate scores for all species for a given play area.

    Args:
        play_area: A dictionary representing the player's arboretum.

    Returns:
        A dictionary with each species and its calculated score.
    """
    all_species = ["J", "R", "C", "M", "O", "W"]
    final_scores = {}

    print("Calculating scores for the provided Arboretum...")
    for species in all_species:
        final_scores[species] = score_play_area(play_area, species)

    return final_scores


def calculate_scoring_probability(species: Species, state: dict) -> float:
    seen_cards = (
        state["hand"]
        + state["opponentHand"]
        + state["discard"]
        + state["opponentDiscard"]
        + list(y for x in state["playArea"].values() for y in x.values())
        + list(y for x in state["opponentPlayArea"].values() for y in x.values())
    )

    unknown_cards = ALL_CARDS - {tuple(card) for card in seen_cards if not card is None}
    num_unknown_cards_op = state["opponentHand"].count(None)
    possible_missing_cards_combos = list(
        combinations(unknown_cards, num_unknown_cards_op)
    )
    my_score = calc_hand_score(species, state["hand"])
    probs = []
    for combo in possible_missing_cards_combos:
        op_hand = [card for card in state["opponentHand"] if not card is None] + list(
            combo
        )
        if my_score < calc_hand_score(species, op_hand):
            probs.append(1 / len(possible_missing_cards_combos))
    return sum(probs)


def calc_hand_score(species: Species, hand: list[Card]) -> int:
    return sum([card[1] for card in hand if card[0] == species])


def calc_prob_opponent_has_card_in_hand(card: Card, state: dict) -> float:
    seen_cards_not_op_hand = (
        state["hand"]
        + list(y for x in state["playArea"].values() for y in x.values())
        + list(y for x in state["opponentPlayArea"].values() for y in x.values())
    )
    seen_cards_op_hand = state["opponentHand"]
    deck_size = state["deck"]

    if card in seen_cards_not_op_hand:
        return 0
    if card in seen_cards_op_hand:
        return 1
    num_unknown_cards_op_hand = state["opponentHand"].count(None)
    return num_unknown_cards_op_hand / (deck_size + num_unknown_cards_op_hand)


def get_weighted_scores(state: dict) -> dict[Species, float]:
    scores = calculate_all_scores(state["playArea"])
    return {
        species: score * calculate_scoring_probability(species, state)
        for species, score in scores.items()
    }


# --- Execution ---
if __name__ == "__main__":
    # Your input dictionary
    #
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

    for s in ["J", "R", "C", "M", "O", "W"]:
        print(s)
        print(calculate_scoring_probability(s, test_state))
    player_arboretum = {
        "0": {
            "0": ["C", 1],
            "1": ["J", 8],
            "2": ["W", 3],
            "-1": ["O", 7],
            "-2": ["O", 5],
        },
        "1": {
            "0": ["M", 3],
            "1": ["C", 8],
            "2": ["R", 2],
            "-1": ["R", 1],
            "-2": ["R", 6],
        },
        "2": {
            "0": ["M", 1],
            "1": ["C", 4],
            "2": ["W", 5],
            "-2": ["J", 4],
            "-1": ["R", 8],
        },
        "-1": {"-2": ["J", 7]},
    }

    # Calculate and print the scores

    scores = calculate_all_scores(player_arboretum)

    print("\n--- Final Scores ---")
    for species, score in scores.items():
        print(f"Species {species}: {score} points")
    print("--------------------")

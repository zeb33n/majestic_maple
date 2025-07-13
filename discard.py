from copy import deepcopy
import place
from utils import get_valid_play_coordinates
from scoring import get_weighted_scores
import sys


def eprint(*args, **kwargs):
    """Prints to stderr."""
    print(*args, file=sys.stderr, **kwargs)


def get_cached_card_rankings():
    """
    Returns cached card rankings from place.py, sorted by score (lowest first).
    
    Returns:
        List of (card, score) tuples sorted by score ascending
    """
    return sorted(place.cached_card_scores, key=lambda x: x[1])


def assess_card_placement_for_opponent(card, coord, state):
    """
    Simulates placing a card on the opponent's tableau and returns the score.
    
    Args:
        card: Card tuple [species, rank]
        coord: Coordinate tuple (x, y) 
        state: Game state dictionary
    
    Returns:
        Float score that opponent would get from this placement
    """
    # Create a copy of the state for simulation
    state_copy = deepcopy(state)
    
    # Place the card on opponent's play area
    x_key = str(coord[0])
    y_key = str(coord[1])
    
    opponent_area = state_copy["opponentPlayArea"]
    if x_key in opponent_area:
        opponent_area[x_key][y_key] = card
    else:
        opponent_area[x_key] = {y_key: card}
    
    # Calculate weighted scores for opponent's modified tableau
    # We need to create a state where opponent's area is treated as the main play area
    # Filter out None values from opponent's hand
    opponent_hand_filtered = [card for card in state_copy["opponentHand"] if card is not None]
    
    opponent_state = {
        "playArea": state_copy["opponentPlayArea"],
        "hand": opponent_hand_filtered,
        "discard": state_copy["opponentDiscard"],
        "opponentHand": state_copy["hand"],
        "opponentDiscard": state_copy["discard"],
        "opponentPlayArea": state_copy["playArea"],
        "deck": state_copy["deck"],
        "turn": state_copy["turn"],
        "subTurn": state_copy["subTurn"],
        "previousTurn": state_copy["previousTurn"]
    }
    
    weighted_scores = get_weighted_scores(opponent_state)
    return sum(weighted_scores.values())


def get_opponent_best_score_for_card(card, state):
    """
    Finds the best possible score the opponent could achieve by placing this card.
    
    Args:
        card: Card tuple [species, rank]
        state: Game state dictionary
    
    Returns:
        Float representing the highest score opponent could get with this card
    """
    coords = get_valid_play_coordinates(state["opponentPlayArea"])
    best_score = 0
    
    for coord in coords:
        score = assess_card_placement_for_opponent(card, coord, state)
        if score > best_score:
            best_score = score
    
    return best_score


def get_discard_card(state, num_candidates=4):
    """
    Determines the best card to discard using opponent simulation heuristic.
    
    Args:
        state: Game state dictionary
        num_candidates: Number of worst-scoring cards to evaluate (default 4)
    
    Returns:
        Card tuple [species, rank] that should be discarded
    """
    # Get our cached rankings (lowest scores first)
    rankings = get_cached_card_rankings()
    
    if not rankings:
        eprint("Warning: No cached rankings available. Call get_best_play() first.")
        return state["hand"][0] if state["hand"] else None
    
    # Take the worst N cards from our perspective
    candidates = rankings[:min(num_candidates, len(rankings))]
    
    if not candidates:
        return state["hand"][0] if state["hand"] else None
    
    # Evaluate each candidate from opponent's perspective
    opponent_scores = []
    for card, our_score in candidates:
        opponent_best_score = get_opponent_best_score_for_card(card, state)
        opponent_scores.append((card, opponent_best_score))
        eprint(f"Card {card}: Our score={our_score:.2f}, Opponent best score={opponent_best_score:.2f}")
    
    # Sort by opponent score (lowest first) - we want to discard the card 
    # that gives the opponent the least benefit
    opponent_scores.sort(key=lambda x: x[1])
    
    discard_card = opponent_scores[0][0]
    print(f"Discard: {discard_card}")
    
    return discard_card


if __name__ == "__main__":
    # Test with the state from place.py
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
    
    # First call get_best_play to populate cache
    best_play = place.get_best_play(test_state)
    print(f"Best play: {best_play}")
    
    # Then get discard recommendation
    discard_card = get_discard_card(test_state)
import copy
import random
from typing import List, Dict

from data_structures import Card, Move
from placement import get_valid_placements
from scoring import get_weighted_scores


def find_best_play(hand: List[Card], tableau: Dict) -> Move:
    """
    Analyzes all possible card placements and returns the one that yields
    the highest weighted score improvement. The discard choice is random.
    """
    best_move = None
    best_score_improvement = -float('inf')

    # The scoring function requires a full state dictionary. We build a
    # simplified one with the data we have.
    def build_state(current_hand, current_tableau):
        # Convert hand and tableau to the tuple format expected by scoring.py
        hand_tuples = [(c.species, c.value) for c in current_hand]
        tableau_tuples = {
            x: {y: (card.species, card.value) for y, card in y_dict.items()}
            for x, y_dict in current_tableau.items()
        }
        return {
            "hand": hand_tuples,
            "playArea": tableau_tuples,
            # Provide empty/default values for other required keys
            "opponentHand": [],
            "discard": [],
            "opponentDiscard": [],
            "opponentPlayArea": {},
            "deck": 0
        }

    base_state = build_state(hand, tableau)
    base_score = sum(get_weighted_scores(base_state).values())
    
    valid_placements = get_valid_placements(tableau)

    for i, play_card in enumerate(hand):
        remaining_hand = hand[:i] + hand[i+1:]
        if not remaining_hand:
            continue
        
        for placement in valid_placements:
            hypothetical_tableau = copy.deepcopy(tableau)
            x, y = placement
            if x not in hypothetical_tableau:
                hypothetical_tableau[x] = {}
            hypothetical_tableau[x][y] = play_card
            
            # After playing a card, the hand for the next state is the remaining hand
            hypothetical_state = build_state(remaining_hand, hypothetical_tableau)
            
            new_weighted_scores = get_weighted_scores(hypothetical_state)
            new_score = sum(new_weighted_scores.values())
            
            score_improvement = new_score - base_score

            if score_improvement > best_score_improvement:
                best_score_improvement = score_improvement
                discard_card = random.choice(remaining_hand)
                best_move = Move(play_card, placement, discard_card)

    if best_move is None and hand:
        play_card = random.choice(hand)
        remaining_hand = [c for c in hand if c != play_card]
        if remaining_hand and valid_placements:
            discard_card = random.choice(remaining_hand)
            placement = random.choice(valid_placements)
            best_move = Move(play_card, placement, discard_card)

    return best_move


if __name__ == '__main__':
    print("--- Running Move Evaluator Standalone Test (with real scoring) ---")

    test_state_data = {
        "hand": [["R", 1], ["J", 3], ["R", 4], ["J", 5], ["O", 4], ["J", 4], ["R", 3]],
        "playArea": {
            "0": {"0": ["W", 2], "1": ["C", 6], "2": ["R", 7], "-1": ["M", 8]},
            "1": {"0": ["O", 6], "1": ["M", 4], "2": ["O", 1], "-1": ["O", 5]},
            "2": {"0": ["J", 2], "1": ["J", 6], "-1": ["M", 2]},
            "-1": {"0": ["R", 6], "1": ["C", 4], "-1": ["C", 3]},
            "-2": {"1": ["C", 2]},
        },
    }

    sample_hand = [Card(s, v) for s, v in test_state_data["hand"]]
    sample_tableau = {
        x: {y: Card(c[0], c[1]) for y, c in y_dict.items()}
        for x, y_dict in test_state_data["playArea"].items()
    }

    print(f"Hand: {[f'{c.species}{c.value}' for c in sample_hand]}")
    
    best_play_found = find_best_play(sample_hand, sample_tableau)

    if best_play_found:
        print("\nBest play found:")
        print(f"  Play Card: {best_play_found.play_card.species}{best_play_found.play_card.value}")
        print(f"  Placement: {best_play_found.placement}")
        print(f"  Discard Card (Random): {best_play_found.discard_card.species}{best_play_found.discard_card.value}")
    else:
        print("\nNo valid play was found.")

    print("\n--- Test Complete ---")
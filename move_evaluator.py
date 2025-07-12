import copy
from typing import List, Dict

from data_structures import Card, Move
from placement import get_valid_placements
# We will assume scoring.py has these functions.
# We will create placeholder functions here for now.
# from scoring import calculate_total_path_score, calculate_discard_cost

# Placeholder scoring functions for standalone testing
def calculate_total_path_score(tableau: Dict) -> int:
    """Placeholder for the real path scoring function."""
    # A simple heuristic: number of cards in tableau
    return sum(len(y_dict) for y_dict in tableau.values())

def calculate_discard_cost(opponent_tableau: Dict, discard_card: Card) -> int:
    """Placeholder for the real discard cost function."""
    # A simple heuristic: returns the value of the card, making high cards costly to discard
    return discard_card.value


def find_best_move(hand: List[Card], tableau: Dict, opponent_tableau: Dict) -> Move:
    """
    Analyzes all possible moves and returns the one with the highest score.

    A move consists of playing a card to the tableau and discarding another.
    The score is calculated as:
    (score of new tableau) - (score of current tableau) - (cost of discard)
    """
    best_move = None
    best_score = -float('inf')

    current_tableau_score = calculate_total_path_score(tableau)
    valid_placements = get_valid_placements(tableau)

    # Loop 1: Iterate through each card in hand to consider it for playing
    for i, play_card in enumerate(hand):
        
        # Create the remaining hand after selecting a play_card
        remaining_hand = hand[:i] + hand[i+1:]
        
        # Loop 2: Iterate through all valid placements on the board
        for placement in valid_placements:
            
            # Create a hypothetical new tableau with the card placed
            hypothetical_tableau = copy.deepcopy(tableau)
            x, y = placement
            if x not in hypothetical_tableau:
                hypothetical_tableau[x] = {}
            hypothetical_tableau[x][y] = play_card
            
            new_tableau_score = calculate_total_path_score(hypothetical_tableau)
            path_improvement_score = new_tableau_score - current_tableau_score

            # Loop 3: Iterate through remaining cards to consider for discarding
            for discard_card in remaining_hand:
                
                discard_penalty = calculate_discard_cost(opponent_tableau, discard_card)
                
                current_score = path_improvement_score - discard_penalty

                if current_score > best_score:
                    best_score = current_score
                    best_move = Move(play_card, placement, discard_card)

    return best_move


if __name__ == '__main__':
    # This block allows for standalone testing of the move evaluator.
    # It uses the sample data from the game_engine_reference.md.
    print("--- Running Move Evaluator Standalone Test ---")

    # Player's hand (9 cards, must play 1 and discard 1)
    sample_hand = [
        Card("J", 8), Card("R", 5), Card("C", 7), Card("M", 2), Card("M", 6),
        Card("O", 1), Card("O", 8), Card("W", 4), Card("W", 7)
    ]

    # Player's current tableau
    sample_tableau = {
        -1: {
            -1: Card("W", 3),
            0: Card("J", 4),
            1: Card("O", 6)
        },
        0: {
            0: Card("C", 2),
            1: Card("O", 5)
        },
        1: {
            0: Card("J", 3)
        }
    }

    # Opponent's tableau (for discard cost calculations)
    sample_opponent_tableau = {
        0: {
            0: Card("M", 4),
            1: Card("J", 1),
            2: Card("O", 2)
        },
        1: {
            0: Card("M", 3),
            1: Card("O", 5),
            2: Card("J", 4)
        },
        2: {
            1: Card("O", 3)
        }
    }

    print(f"Initial hand size: {len(sample_hand)}")
    print(f"Initial tableau card count: {sum(len(y) for y in sample_tableau.values())}")
    
    # Find the best move
    best_move_found = find_best_move(sample_hand, sample_tableau, sample_opponent_tableau)

    if best_move_found:
        print("\nBest move found:")
        print(f"  Play Card: {best_move_found.play_card.species}{best_move_found.play_card.value}")
        print(f"  Placement: {best_move_found.placement}")
        print(f"  Discard Card: {best_move_found.discard_card.species}{best_move_found.discard_card.value}")
    else:
        print("\nNo valid move was found.")

    print("\n--- Test Complete ---")
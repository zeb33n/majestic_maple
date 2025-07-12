import sys
import json
import time
import random
from copy import deepcopy

from mcts_node import MCTSNode
from data_structures import Card, Move
from placement import get_valid_placements
from scoring import score_play_area

# --- Configuration ---
TIME_LIMIT_SECONDS = 1.2  # As per the project spec

# --- Data Conversion Helpers ---

def json_to_py(data):
    """Converts the incoming JSON state to our Python objects."""
    hand = [Card(c[0], c[1]) for c in data['hand']]
    play_area = {
        x: {y: Card(card[0], card[1]) for y, card in y_dict.items()}
        for x, y_dict in data['playArea'].items()
    }
    opponent_play_area = {
        x: {y: Card(card[0], card[1]) for y, card in y_dict.items()}
        for x, y_dict in data['opponentPlayArea'].items()
    }
    # Create a list of all cards not visible to the player
    seen_cards = {tuple(c) for c in data['hand']}
    for pa in [play_area, opponent_play_area, data['discard'], data['opponentDiscard']]:
        if isinstance(pa, dict):
            for row in pa.values():
                for card in row.values():
                    seen_cards.add((card.species, card.value))
        else: # It's a list (discard pile)
            for card in pa:
                seen_cards.add(tuple(card))

    # A full deck for Arboretum with 6 species
    all_cards = [(s, v) for s in ["J", "R", "C", "M", "O", "W"] for v in range(1, 9)]
    deck = [Card(s, v) for s, v in all_cards if (s, v) not in seen_cards]
    random.shuffle(deck)

    return {
        'player_hand': hand,
        'player_tableau': play_area,
        'opponent_tableau': opponent_play_area,
        'deck': deck
    }

def py_to_json(move: Move):
    """Converts our chosen Move object back to the required JSON format."""
    return {
        "card": [move.play_card.species, move.play_card.value],
        "coord": [int(move.placement[0]), int(move.placement[1])]
    }

# --- MCTS Core Logic ---

def run_mcts(initial_state):
    """The main MCTS process."""
    root = MCTSNode(initial_state)
    end_time = time.time() + TIME_LIMIT_SECONDS

    while time.time() < end_time:
        # 1. Selection: Start from the root and find the best leaf node
        leaf = select_leaf(root)
        
        # 2. Expansion: If the leaf is not terminal, expand it
        if not leaf.is_fully_expanded():
            child = leaf.expand()
            if child:
                # 3. Simulation (Playout)
                result = simulate_playout(child)
                # 4. Backpropagation
                backpropagate(child, result)

    # After time is up, choose the best move based on visits
    best_child = max(root.children, key=lambda c: c.visits, default=None)
    return best_child.move_that_led_here if best_child else None

def select_leaf(node):
    """Traverse the tree using UCT scores to find a leaf node."""
    while node.children:
        if not node.is_fully_expanded():
            return node.expand()
        node = max(node.children, key=lambda c: c.calculate_uct_score())
    return node

def simulate_playout(node):
    """
    Simulates a random game from a node to the end and returns the score differential.
    This is the "Monte Carlo" part of MCTS.
    """
    playout_state = deepcopy(node.state)
    
    # The state passed to this function is for the opponent's turn.
    # We alternate turns until the deck is empty.
    current_player_is_opponent = True 

    while playout_state['deck']:
        hand = playout_state['player_hand'] if not current_player_is_opponent else []
        tableau = playout_state['player_tableau'] if not current_player_is_opponent else playout_state['opponent_tableau']

        # Draw 2 cards
        for _ in range(2):
            if playout_state['deck']:
                hand.append(playout_state['deck'].pop())
        
        if len(hand) < 2: break

        # Make a random move (play and discard)
        play_card = random.choice(hand)
        hand.remove(play_card)
        discard_card = random.choice(hand)
        hand.remove(discard_card)
        
        valid_placements = get_valid_placements(tableau)
        placement = random.choice(valid_placements)
        x, y = placement
        if x not in tableau: tableau[x] = {}
        tableau[x][y] = play_card

        # Swap perspective for the next turn
        current_player_is_opponent = not current_player_is_opponent

    # Game over, calculate final score
    my_final_score = sum(score_play_area(playout_state['player_tableau'], s) for s in ["J", "R", "C", "M", "O", "W"])
    op_final_score = sum(score_play_area(playout_state['opponent_tableau'], s) for s in ["J", "R", "C", "M", "O", "W"])
    
    return my_final_score - op_final_score

def backpropagate(node, result):
    """Update statistics up the tree from the simulation result."""
    # The result is from the perspective of the parent of the simulated node.
    # We need to alternate the sign of the result as we go up.
    while node is not None:
        node.update(result)
        result = -result # The score for the parent is the inverse of the child's
        node = node.parent

# --- Main Execution ---

if __name__ == "__main__":
    # 1. Read and parse the input from the game engine
    try:
        input_json = sys.stdin.read()
        data = json.loads(input_json)
        message_id = data.get("messageID")
        state_data = data.get("state", {})
    except (json.JSONDecodeError, KeyError) as e:
        # If input is invalid, we can't proceed.
        # eprint(f"Error reading input: {e}")
        exit()

    # 2. Route based on the sub-turn
    sub_turn = state_data.get("subTurn")
    
    if sub_turn == 2:
        # Time to think: convert state and run MCTS
        initial_state = json_to_py(state_data)
        
        # The hand from the engine has 7 cards. We draw 2 before playing.
        for _ in range(2):
            if initial_state['deck']:
                initial_state['player_hand'].append(initial_state['deck'].pop())

        best_move = run_mcts(initial_state)
        
        if best_move:
            output = {"move": py_to_json(best_move), "messageID": message_id}
        else:
            # Fallback to random if MCTS fails
            output = {"move": "RANDOM", "messageID": message_id}
    else:
        # For drawing and discarding, respond randomly as per the plan
        output = {"move": "RANDOM", "messageID": message_id}

    # 3. Print the final move to stdout
    print(json.dumps(output))

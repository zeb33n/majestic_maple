import numpy as np
import random
from copy import deepcopy

# Assuming these helpers exist and are correctly implemented
from placement import get_valid_placements
from data_structures import Card, Move

class MCTSNode:
    """
    A class representing a single node in the Monte Carlo Search Tree.
    Each node corresponds to a stable game state, ready for a player to make a move.
    """
    def __init__(self, state, parent=None, move_that_led_here=None):
        """
        Initializes a new MCTS node.
        :param state: A dictionary representing the game state. Expected keys:
                      'player_hand', 'player_tableau', 'opponent_tableau', 'deck'.
        :param parent: The parent node in the tree.
        :param move_that_led_here: The complete (play, place, discard) move that led to this state.
        """
        self.state = state
        self.parent = parent
        self.move_that_led_here = move_that_led_here
        self.children = []
        
        # A list of all complete, possible moves from this state.
        self.untried_moves = self.get_all_possible_moves()
        
        # MCTS statistics
        self.wins = 0  # For our purpose, this will be the sum of score differentials
        self.visits = 0

    def get_all_possible_moves(self):
        """
        Generates all possible, complete moves (play, place, discard) from this state.
        This is a potentially large list, representing all actions for one turn.
        """
        possible_moves = []
        hand = self.state['player_hand']
        tableau = self.state['player_tableau']
        
        # After drawing, the hand has 9 cards. We must play 1 and discard 1.
        # If hand size is different, this logic might need adjustment.
        if len(hand) < 2:
            return []

        valid_placements = get_valid_placements(tableau)

        for i, play_card in enumerate(hand):
            remaining_hand = hand[:i] + hand[i+1:]
            for placement in valid_placements:
                for discard_card in remaining_hand:
                    possible_moves.append(Move(play_card, placement, discard_card))
        
        random.shuffle(possible_moves) # Shuffle to ensure random exploration
        return possible_moves

    def calculate_uct_score(self, exploration_constant=1.414):
        """
        Calculates the UCT score for this node, balancing exploitation and exploration.
        """
        if self.visits == 0:
            return float('inf')  # Prioritize unvisited nodes
        
        # Exploitation term: average win score
        win_rate = self.wins / self.visits
        
        # Exploration term: favors less-visited nodes
        exploration_term = exploration_constant * np.sqrt(
            np.log(self.parent.visits) / self.visits
        )
        
        return win_rate + exploration_term

    def expand(self):
        """
        Expands the tree by creating a new child node from an untried move.
        """
        if not self.untried_moves:
            return None # Should not happen if called correctly

        move = self.untried_moves.pop()
        
        # Create the next state by applying the move
        next_state = deepcopy(self.state)
        
        # Apply the play card to the tableau
        play_card, placement, discard_card = move
        x, y = placement
        if x not in next_state['player_tableau']:
            next_state['player_tableau'][x] = {}
        next_state['player_tableau'][x][y] = play_card
        
        # Update the hand
        next_state['player_hand'].remove(play_card)
        next_state['player_hand'].remove(discard_card)

        # The new state is now ready for the *opponent's* turn.
        # For simplicity in this model, we swap perspectives.
        child_state_for_opponent = {
            'player_hand': [], # We don't know the opponent's hand
            'player_tableau': next_state['opponent_tableau'],
            'opponent_tableau': next_state['player_tableau'],
            'deck': next_state['deck']
        }

        child = MCTSNode(state=child_state_for_opponent, parent=self, move_that_led_here=move)
        self.children.append(child)
        return child

    def update(self, result):
        """
        Updates the node's statistics from a simulation result.
        """
        self.visits += 1
        self.wins += result

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def __repr__(self):
        return f"[Node: Move={self.move_that_led_here}, W/V={self.wins}/{self.visits}, Children={len(self.children)}]"

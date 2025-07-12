# MCTS Bot Implementation Plan

## Overview

This is the architectural plan for building a Monte Carlo Tree Search (MCTS) bot for Arboretum. Unlike Deep Learning models that require training, the MCTS bot is a search algorithm that performs its "thinking" live during the 1.2 seconds it has to make a move. The bot builds and refines its search tree from scratch for every single move.

## Architecture

### Core Components

1. **GameRunner (main.py)**: The top-level script that sets up a game between the MCTS bot and an opponent bot, then runs the main game loop.

2. **MCTSBot (mcts_bot.py)**: The public-facing part of the agent with the crucial method `choose_move(game_state, time_limit)`. Houses the main MCTS logic (the timed loop).

3. **MCTSNode (mcts_node.py)**: A simple class representing a single node in the search tree. Data container for visits, scores, parent/child relationships, and the move that led to it.

4. **HeuristicEvaluator (heuristic_evaluator.py)**: Contains the "brain" of the bot with functions for scoring moves and evaluating states (`score_move`, `calculate_path_improvement`, etc.). Used extensively during the simulation phase.

5. **GameState Utilities (game_state.py)**: Lightweight, fast-to-copy internal representation of the game state for thousands of simulations.

## Implementation Plan

### Day 1: Building the Engine

**Goal:** Fully functional MCTS bot that can play a complete game, even if poorly.

#### Step 1: The Foundation (Data Structures)
**File:** `game_state.py`
- Define internal game state classes (lightweight and simple)
- `Card(species: int, value: int)`
- `PlayerState(hand: List[Card], tableau: Dict[(x,y), Card], discard: List[Card])`
- `GameState(players: List[PlayerState], draw_pile: List[Card], current_player_idx: int)`
- Add `determinization()` method to shuffle unknown cards

#### Step 2: The Tree Node
**File:** `mcts_node.py`
- Create `MCTSNode` class with attributes: parent, children, move_that_led_here, visit_count, total_score
- Implement `calculate_uct_score()` method (UCT formula)

#### Step 3: The MCTS Skeleton
**File:** `mcts_bot.py`
- Build core MCTS search loop with RANDOM playout policy
- Create `MCTSBot` class with `choose_move(state, time_limit)` method
- Implement timed while loop (~1.2 seconds)
- Four phases:
  1. **Selection**: Move to child with highest UCT score until reaching leaf
  2. **Expansion**: Create new child node for untried moves
  3. **Simulation**: Random playout to game end (temporary)
  4. **Backpropagation**: Update visit_count and total_score back to root
- Return move from root's most visited child

### Day 2: Making it Intelligent

**Goal:** Replace random simulation with smart heuristics and tune strategy.

#### Step 4: The Heuristic Brain
**File:** `heuristic_evaluator.py`
- Create dictionary of WEIGHTS
- Implement `calculate_path_improvement(tableau, card_to_play)`
- Implement `calculate_scoring_right_confidence(...)`
- Implement `calculate_discard_cost(opponent_tableau, discard_card)`
- Combine into master `score_move(state, play_card, discard_card)` function

#### Step 5: The Brain Transplant (Integration)
**File:** `mcts_bot.py`
- Replace random playout logic with smart playout
- In simulation loop: call `heuristic_evaluator.score_move` for all legal moves
- Choose move with highest returned score

#### Step 6: The Game Runner & Tuning
**File:** `main.py`
- Finalize game runner to pit MCTSBot against other heuristic bots
- Run many games and observe behavior
- Tune WEIGHTS in `heuristic_evaluator.py` based on performance

## Current Implementation Status

- **I/O**: Using readline for all input/output operations
- **Scoring**: Heuristics system implemented
- **Focus**: Real-time search algorithm that builds strategy during gameplay

This modular design allows for parallel development and clear separation of concerns, progressing from a basic framework to an intelligent agent.
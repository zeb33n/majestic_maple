# MCTS Arboretum Bot Project

## Project Overview

This project involves building a Monte Carlo Tree Search (MCTS) bot for the card game Arboretum within the Hackaranda tournament framework. The bot performs real-time search during gameplay rather than using pre-trained models.

## Key Technologies

- **I/O**: readline for all input/output operations
- **Scoring**: Custom heuristics system implemented
- **Architecture**: Real-time search algorithm that builds strategy during gameplay
- **Language**: Python for the MCTS bot implementation
- **Framework**: Node.js/TypeScript Hackaranda tournament system

## Project Structure

- `hackaranda.md`: Complete overview of the tournament framework
- `workplan.md`: Detailed MCTS implementation architecture and plan
- Bot implementation files (to be created):
  - `main.py`: Game runner
  - `mcts_bot.py`: Main MCTS algorithm
  - `mcts_node.py`: Tree node representation
  - `heuristic_evaluator.py`: Scoring and evaluation logic
  - `game_state.py`: Game state utilities

## Important Commands

- `npm install`: Install dependencies
- `npm run build`: Compile TypeScript
- `npm start`: Launch CLI interface
- Build default bots option in CLI for first-time setup

## Development Notes

- The MCTS bot performs search in real-time (1.2 second time limit per move)
- No training phase - algorithm builds search tree from scratch each move
- Modular design allows parallel development
- Focus on fast, lightweight game state representation for simulations

## Arboretum Game Rules

### Overview
Arboretum is a strategic card game where players build tree-lined paths (arboretums) and secure the right to score those paths by having the highest total value of matching cards in hand at the end of the game.

### Game Components
- **Deck**: 80 cards, 10 species (each numbered 1–8)
- **Player count variants**:
  - 2 players: 6 species (48 cards)
  - 3 players: 8 species (64 cards)  
  - 4 players: 10 species (80 cards)

### Setup
- Shuffle the deck
- Each player is dealt 7 cards
- Remaining cards form a central draw pile
- Each player has a personal discard pile

### Turn Structure
1. **Draw 2 cards**: From draw pile or any player's discard pile (including your own)
   - You may look at the first card before choosing the second source
2. **Play 1 card** into your arboretum:
   - First card can go anywhere
   - Subsequent cards must be placed orthogonally adjacent to existing cards
3. **Discard 1 card** to your own discard pile (face up)
   - Hand size must always end at 7 cards

### Game End
Game ends when the last card from the draw pile is drawn. Final turn finishes, then scoring begins.

### Scoring System

#### Scoring Rights
- For each tree species, only the player with the highest total sum of that species **in hand** gets to score a path of that species
- Ties allow all tied players to score that species
- **"1 vs 8 Rule"**: If Player A holds a '1' of a species and Player B holds an '8' of the same species, B's 8 is worth 0 for scoring rights
- If no one holds any cards of a species in hand, everyone may score a path of that species

#### Valid Paths
A valid path must:
- Start and end with the same species
- Cards must be in strictly ascending numerical order
- Must be orthogonally adjacent (no diagonals)
- Can include cards of other species in the middle
- Only one path per species may be scored

#### Points Awarded
- +1 point per card in the path
- +1 per card if path is 4+ cards of the same species (doubling the base)
- +1 point if path starts with a "1" of that species
- +2 points if path ends with an "8" of that species
- Cards may be used in multiple paths

### Winning
- Player with the highest total score wins
- **Tie-breaker 1**: Player with the most different species in their arboretum wins
- **Tie-breaker 2**: If still tied, players share the victory

### Strategic Highlights
Players must balance:
- Building high-value paths in the arboretum
- Holding cards in hand to win scoring rights
- Denying opponents key cards or scoring opportunities
- Discarding carefully (valuable cards may help opponents)
- Perfect tracking of played and discarded cards is advantageous
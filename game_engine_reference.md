# Game Engine Data Structures & Commands Reference

## Overview

This document provides a comprehensive reference for all data types, structures, and logic used by the Arboretum game engine. This serves as the definitive guide for implementing the MCTS bot's `move_evaluator.py` and ensuring compatibility with the main repository's game engine.

## Core Data Structure Definitions

### Card

**Repository Representation:** A card is represented as a JSON array (or tuple) of `[species, rank]`.

**TypeScript Definition:** 
```typescript
type Card = [species, rank];
```

**Python Equivalent:** 
```python
from collections import namedtuple
Card = namedtuple('Card', ['species', 'value'])
```

**Data Details:**
- **species**: A single uppercase character string representing the tree type:
  - `"J"`: Jacaranda
  - `"R"`: Royal Poinciana  
  - `"C"`: Cassia
  - `"M"`: Maple
  - `"O"`: Oak
  - `"W"`: Willow
- **value** (or `rank`): An integer from `1` to `8`

**Sample JSON Data:**
```json
["M", 5]
```

**Python Usage:**
```python
card = Card("M", 5)  # Maple 5
print(card.species)  # "M"
print(card.value)    # 5
```

### Move

**Conceptual Structure:** A complete move in Arboretum consists of playing a card and discarding a card. While the repository handles these as separate actions, your evaluator should treat them as a unified move.

**Python Definition:**
```python
Move = namedtuple('Move', ['play_card', 'placement', 'discard_card'])
```

**Data Details:**
- **play_card**: A `Card` object representing the card being played to the tableau
- **placement**: A tuple of integers `(x, y)` indicating the coordinate position
- **discard_card**: A `Card` object representing the card being discarded

**Usage Example:**
```python
move = Move(
    play_card=Card("J", 3),
    placement=(1, 0),
    discard_card=Card("W", 7)
)
```

### Tableau (Play Area)

**Repository Representation:** Called `playArea` in the codebase. A JSON object where keys are x-coordinates (as strings), and values are objects where keys are y-coordinates (as strings) and values are `Card` arrays.

**TypeScript Definition:**
```typescript
type playArea = Record<number, Record<number, Card>>;
```

**Python Equivalent:**
```python
Dict[int, Dict[int, Card]]
```

**Sample JSON Data:**
```json
{
  "0": {
    "0": ["C", 2]
  },
  "1": {
    "-1": ["C", 6],
    "0": ["J", 3]
  },
  "2": {
    "0": ["R", 6]
  }
}
```

**Python Access Pattern:**
```python
# Check if a card exists at position (1, 0)
if 1 in tableau and 0 in tableau[1]:
    card = tableau[1][0]  # Returns Card object

# Add a card to position (2, 1)
if 2 not in tableau:
    tableau[2] = {}
tableau[2][1] = Card("M", 4)
```

### Hand

**Repository Representation:** A simple JSON array of `Card` objects.

**TypeScript Definition:**
```typescript
type Hand = Card[];
```

**Python Equivalent:**
```python
List[Card]
```

**Sample JSON Data:**
```json
[
  ["J", 8],
  ["O", 6],
  ["O", 5],
  ["O", 4],
  ["O", 1],
  ["W", 3],
  ["J", 2]
]
```

## Core Logic Functions

### Valid Placement Logic

The `get_valid_placements(tableau)` function is crucial for determining legal moves.

**Rules:**
1. **Empty Tableau**: If the tableau is empty, only position `(0, 0)` is valid
2. **Non-Empty Tableau**: A position `(x, y)` is valid if:
   - The coordinate is currently empty (not occupied)
   - The coordinate is orthogonally adjacent (up, down, left, right) to at least one existing card

**Implementation Pseudocode:**
```python
def get_valid_placements(tableau):
    if not tableau:  # Empty tableau
        return [(0, 0)]
    
    valid_placements = set()
    
    # Get all occupied coordinates
    occupied_coords = []
    for x in tableau:
        for y in tableau[x]:
            occupied_coords.append((x, y))
    
    # Check neighbors of each occupied position
    for x, y in occupied_coords:
        # Check four orthogonal directions
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor_x, neighbor_y = x + dx, y + dy
            
            # Check if neighbor is empty
            if (neighbor_x not in tableau or 
                neighbor_y not in tableau.get(neighbor_x, {})):
                valid_placements.add((neighbor_x, neighbor_y))
    
    return list(valid_placements)
```

### Coordinate System

**Important Notes:**
- Coordinates can be negative (e.g., `(-1, -2)` is valid)
- Origin `(0, 0)` is the starting position for the first card
- X-axis: horizontal (left-right)
- Y-axis: vertical (up-down)
- Only orthogonal adjacency is allowed (no diagonals)

## Sample Data for Testing

### Complete Test Scenario

```python
# Player's hand after drawing 2 cards (9 cards total, must discard 1)
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
```

### Expected Valid Placements

For `sample_tableau`, the `get_valid_placements()` function should return coordinates including:
- `(-2, -1)`, `(-1, -2)`, `(-1, 2)`: Adjacent to cards at `(-1, -1)`, `(-1, 0)`, `(-1, 1)`
- `(0, -1)`, `(0, 2)`: Adjacent to cards at `(0, 0)`, `(0, 1)`
- `(1, -1)`, `(1, 1)`: Adjacent to card at `(1, 0)`
- `(2, 0)`: Adjacent to card at `(1, 0)`

*Note: Order may vary depending on implementation*

## Integration Notes

### JSON to Python Conversion

When receiving data from the game engine:

```python
def json_to_card(json_card):
    """Convert JSON card format to Python Card namedtuple"""
    return Card(json_card[0], json_card[1])

def json_to_tableau(json_tableau):
    """Convert JSON tableau to Python dictionary"""
    tableau = {}
    for x_str, y_dict in json_tableau.items():
        x = int(x_str)
        tableau[x] = {}
        for y_str, card_json in y_dict.items():
            y = int(y_str)
            tableau[x][y] = json_to_card(card_json)
    return tableau
```

### Python to JSON Conversion

When sending moves back to the game engine:

```python
def card_to_json(card):
    """Convert Python Card to JSON format"""
    return [card.species, card.value]

def move_to_json(move):
    """Convert Python Move to JSON format expected by engine"""
    return {
        "play_card": card_to_json(move.play_card),
        "placement": move.placement,
        "discard_card": card_to_json(move.discard_card)
    }
```

## Usage in move_evaluator.py

This reference enables you to:

1. **Parse incoming game state** from JSON to Python objects
2. **Generate valid moves** using placement logic
3. **Evaluate move quality** using heuristic functions
4. **Convert results** back to JSON for the game engine

The data structures and logic described here are directly compatible with the main repository's game engine and should be used as the authoritative reference for all bot implementations.
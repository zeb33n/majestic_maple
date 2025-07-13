#!/usr/bin/env python3

import json
import sys
from readLine import randomIsh

def test_placement_and_discard():
    """Test the integrated placement and discard logic with actual game format"""
    
    # Sample game state in the format that place() expects (actual gameplay format)
    game_data = {
        "messageID": "test-123",
        "state": {
            "deck": 28,
            "hand": [["W", 2], ["R", 8], ["C", 4], ["J", 4], ["M", 2], ["O", 2], ["W", 4]],
            "discard": [["C", 3]],
            "opponentDiscard": [["J", 2]],
            "playArea": {
                "0": {"0": ["W", 5]},
                "1": {"0": ["W", 6]}
            },
            "opponentPlayArea": {
                "0": {"0": ["J", 8]},
                "-1": {"0": ["O", 8]}
            },
            "opponentHand": [["R", 1], ["C", 2], ["M", 6], ["W", 7], ["O", 6], ["J", 3], ["M", 4]],
            "turn": 6,
            "subTurn": 2,  # Placement phase
            "activeTurn": True,
            "previousTurn": {"move": ["J", 2], "metaData": False}
        }
    }
    
    print("=== Testing Placement Phase (subTurn 2) ===")
    placement_data = game_data.copy()
    placement_data["state"]["subTurn"] = 2
    
    # Simulate placement
    print("Input JSON:", json.dumps(placement_data, indent=2))
    print("\nCalling randomIsh() for placement...")
    
    # Capture output
    import io
    from contextlib import redirect_stdout
    
    f = io.StringIO()
    with redirect_stdout(f):
        randomIsh(placement_data)
    placement_output = f.getvalue().strip()
    
    print("Placement Output:", placement_output)
    
    print("\n=== Testing Discard Phase (subTurn 3) ===")
    discard_data = game_data.copy()
    discard_data["state"]["subTurn"] = 3
    
    print("Input JSON:", json.dumps(discard_data, indent=2))
    print("\nCalling randomIsh() for discard...")
    
    f = io.StringIO()
    with redirect_stdout(f):
        randomIsh(discard_data)
    discard_output = f.getvalue().strip()
    
    print("Discard Output:", discard_output)


if __name__ == "__main__":
    test_placement_and_discard()
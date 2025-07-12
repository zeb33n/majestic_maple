import json
import sys
from mcts_bot import MCTSBot
from copy import deepcopy


def eprint(*args, **kwargs):
    """Prints to stderr."""
    print(*args, file=sys.stderr, **kwargs)


def beginReadLine():
    while True:
        console_input = input()
        try:
            data = json.loads(console_input)
            match data["state"].get("message"):
                case "NEWGAME" | "ENDGAME":
                    startEndGame(data)
                case None:
                    mctsMove(data)
        except json.JSONDecodeError as e:
            eprint(f"Invalid JSON: {e}")


def startEndGame(data: dict):
    output = {"move": 0, "messageID": data["messageID"]}
    print(json.dumps(output))


def mctsMove(data: dict):
    match data["state"]["subTurn"]:
        case 2:
            # This is the play card phase - use MCTS to find best move
            try:
                mcts_bot = MCTSBot()
                chosen_move = mcts_bot.choose_move(data["state"], time_limit=1.15)
                
                output = {
                    "move": {"card": chosen_move["card"], "coord": chosen_move["coord"]},
                    "messageID": data["messageID"],
                }
                print(json.dumps(output))
            except Exception as e:
                eprint(f"MCTS Error: {e}")
                # Fallback to random move
                output = {"move": "RANDOM", "messageID": data["messageID"]}
                print(json.dumps(output))

        case _:
            # For other phases (draw, discard), use random moves for now
            output = {"move": "RANDOM", "messageID": data["messageID"]}
            print(json.dumps(output))


def _get_valid_play_coordinates(play_area: dict) -> set[tuple[int, int]]:
    """
    Calculates all valid empty coordinates adjacent to existing cards.
    """
    # If the play area is empty, the only valid move is at (0, 0).
    if not play_area:
        return {(0, 0)}

    occupied_coords = set()
    empty_adjacent_coords = set()

    # First, find all currently occupied coordinates.
    # The keys in the JSON are strings, so they must be cast to integers.
    for x_str, row in play_area.items():
        for y_str in row.keys():
            occupied_coords.add((int(x_str), int(y_str)))

    # Now, find all empty spaces adjacent to the occupied ones.
    for x, y in occupied_coords:
        # Check the four adjacent positions (up, down, left, right)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            adj_coord = (x + dx, y + dy)
            if adj_coord not in occupied_coords:
                empty_adjacent_coords.add(adj_coord)

    return empty_adjacent_coords

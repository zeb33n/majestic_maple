def get_valid_placements(tableau):
    """
    Calculates all valid coordinates to place a new card.
    - If the tableau is empty, only ('0', '0') is valid.
    - Otherwise, a placement is valid if it's an empty spot
      orthogonally adjacent to any existing card.
    Coordinates are strings to match game engine JSON format.
    """
    if not tableau:
        return [('0', '0')]

    valid_placements = set()
    occupied_coords = set()

    for x_str in tableau:
        for y_str in tableau[x_str]:
            occupied_coords.add((x_str, y_str))

    for x_str, y_str in occupied_coords:
        x, y = int(x_str), int(y_str)
        # Check four orthogonal directions
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor_x, neighbor_y = x + dx, y + dy
            neighbor_x_str, neighbor_y_str = str(neighbor_x), str(neighbor_y)

            # Check if the neighbor coordinate is empty
            if neighbor_x_str not in tableau or neighbor_y_str not in tableau.get(neighbor_x_str, {}):
                valid_placements.add((neighbor_x_str, neighbor_y_str))

    return list(valid_placements)

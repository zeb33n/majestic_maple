def get_valid_placements(tableau):
    """
    Calculates all valid coordinates to place a new card.
    - If the tableau is empty, only (0, 0) is valid.
    - Otherwise, a placement is valid if it's an empty spot
      orthogonally adjacent to any existing card.
    """
    if not tableau:
        return [(0, 0)]

    valid_placements = set()
    occupied_coords = []

    for x in tableau:
        for y in tableau[x]:
            occupied_coords.append((x, y))

    for x, y in occupied_coords:
        # Check four orthogonal directions
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor_x, neighbor_y = x + dx, y + dy

            # Check if the neighbor coordinate is empty
            if neighbor_x not in tableau or neighbor_y not in tableau.get(neighbor_x, {}):
                valid_placements.add((neighbor_x, neighbor_y))

    return list(valid_placements)

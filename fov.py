import tcod
from globals import Constants


def initialize_fov(game_map):
    # Creating a new TCOD fov map
    fov_map = tcod.map_new(Constants.MAP_WIDTH, Constants.MAP_HEIGHT)

    # Loop through the fov map and set properties according to generated game map.
    for y in range(Constants.MAP_HEIGHT):
        for x in range(Constants.MAP_WIDTH):
            tcod.map_set_properties(fov_map, x, y, game_map.tiles[x][y].transparent, game_map.tiles[x][y].walkable)

    return fov_map


# Calculates fov_map for player position (in main.py)
# Related: Constants.FOV_RECOMPUTE
def recompute_fov(fov_map, x, y, radius, light_walls=True, algorithm=2):
    tcod.map_compute_fov(fov_map, x, y, radius, light_walls, algorithm)

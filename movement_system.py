from globals import Constants
from globals import Globals
from log import LogMessage
import log
import utils


class MovementSystem:
    # Currently this only has one 'static' method so creating a class out of it is unnecessary, but we might
    # add functionality that requires class-scope variables, so let's keep it like this.
    def __init__(self):
        pass

    def update(self, game_map):
        player = False
        player_movement_success = True
        # Loop all entities in array, check if player, update positions
        for entity in Globals.ENTITIES:
            # If player has TagComponent() and a tag called 'PLAYER'
            if entity.tags and 'PLAYER' in entity.tags():
                player = True
            # If has PositionComponent() and MovementComponent() and is waiting for movement
            if entity.position and entity.movement\
                    and (entity.movement.dx != 0 or entity.movement.dy != 0):
                # target_ => Where we want to move
                target_x = entity.position.x+entity.movement.dx
                target_y = entity.position.y+entity.movement.dy

                target_entity = utils.get_entity_at(target_x, target_y)
                can_move = True
                if target_entity and target_entity.collision and target_entity.collision.enabled:
                    can_move = False
                    if 'ENEMY' in target_entity.tags():
                        pass

                # Check that the target is within the map borders, and that we can move to the target tile.
                if 0 <= target_x < Constants.MAP_WIDTH and 0 <= target_y < Constants.MAP_HEIGHT and \
                        game_map.tiles[target_x][target_y].walkable and can_move:
                    entity.position.x = target_x
                    entity.position.y = target_y

                    # If the entity is player and we are rendering only the area around it,
                    # move the current camera position (Giving 4x3 block of buffer area)
                    if player and not Globals.FULL_MAP:

                        if target_x < Globals.CAMERA_CURRENT_X and 6 < Globals.CAMERA_CURRENT_X:
                            Globals.CAMERA_CURRENT_X = entity.position.x
                        elif target_x > Globals.CAMERA_CURRENT_X + 3 and\
                                Globals.CAMERA_CURRENT_X < Constants.MAP_WIDTH-10:
                            Globals.CAMERA_CURRENT_X = entity.position.x - 3

                        if target_y < Globals.CAMERA_CURRENT_Y and 4 < Globals.CAMERA_CURRENT_Y:
                            Globals.CAMERA_CURRENT_Y = entity.position.y
                        elif target_y > Globals.CAMERA_CURRENT_Y + 2 and\
                                Globals.CAMERA_CURRENT_Y < Constants.MAP_HEIGHT-8:
                            Globals.CAMERA_CURRENT_Y = entity.position.y - 2
                    if player:
                        # If we moved the player, we should recompute FOV
                        Globals.FOV_RECOMPUTE = True
                    log.add_message(LogMessage("Moved to {},{}".format(target_x, target_y), (255, 255, 255)))
                else:
                    # Couldn't move entity, most likely a wall at target_
                    log.add_message(LogMessage("This path is blocked", (255, 0, 0)))
                    print("Unable to move {} to {},{}".format(repr(entity), target_x, target_y))
                    if player:
                        player_movement_success = False

                # System has updated, so reset variables
                entity.movement.dx = 0
                entity.movement.dy = 0
        return player_movement_success

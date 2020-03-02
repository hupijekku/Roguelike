from globals import Constants
from globals import Globals
from render_system import RenderSystem
from movement_system import MovementSystem
from input_handlers import handle_keys
from input_handlers import handle_mouse_buttons
from actions import MovementAction
from entity import Entity
from map import Map
from components import *
import fov
import os

# Global variables, yes I'm evil
GAME_WINDOW_MAIN = None
RENDER_SYSTEM = None
MOVEMENT_SYSTEM = None
PLAYER = None
GAME_MAP = None
FOV_MAP = None
INVENTORY_SURFACE = None
LOG_SURFACE = None
MINIMAP_SURFACE = None
CURRENT_ACTION_INDEX = -1


def game_init():
    # Initialize pygame and main window
    pygame.init()
    # File-globals
    global GAME_WINDOW_MAIN, RENDER_SYSTEM, MOVEMENT_SYSTEM, PLAYER, GAME_MAP, FOV_MAP,\
        INVENTORY_SURFACE, LOG_SURFACE, MINIMAP_SURFACE
    # Window starting position
    os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (80, 80)
    # Set display size
    GAME_WINDOW_MAIN = pygame.display.set_mode((Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT))
    INVENTORY_SURFACE = pygame.Surface((Constants.INVENTORY_WIDTH, Constants.INVENTORY_HEIGHT))
    LOG_SURFACE = pygame.Surface((Constants.GAME_WIDTH, Constants.LOG_HEIGHT))
    MINIMAP_SURFACE = pygame.Surface((Constants.MINIMAP_WIDTH, Constants.MINIMAP_HEIGHT))

    # Initialize sprites that need display-mode to be set
    Sprites.FOV_OVERLAY = pygame.Surface(Sprites.WALL.get_size()).convert_alpha()
    Sprites.FOV_OVERLAY.fill((255, 255, 255))
    Sprites.FOV_WALL = Sprites.WALL
    Sprites.FOV_WALL.blit(Sprites.FOV_OVERLAY, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    Sprites.FOV_FLOOR = Sprites.FLOOR
    Sprites.FOV_FLOOR.blit(Sprites.FOV_OVERLAY, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    Sprites.FOV_DOOR = Sprites.DOOR
    Sprites.FOV_DOOR.blit(Sprites.FOV_OVERLAY, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    # Initialize ECS Systems
    RENDER_SYSTEM = RenderSystem(GAME_WINDOW_MAIN, INVENTORY_SURFACE, MINIMAP_SURFACE, LOG_SURFACE)
    MOVEMENT_SYSTEM = MovementSystem()

    # Create a new map
    GAME_MAP = Map(Constants.MAP_WIDTH, Constants.MAP_HEIGHT)
    # Generate the map and add entities to list for looping in systems
    Globals.ENTITIES.extend(GAME_MAP.generate(12))
    # Initialize FOV for the map
    FOV_MAP = fov.initialize_fov(GAME_MAP)

    # Create the player entity
    PLAYER = Entity(
        sprite=SpriteComponent(Sprites.PLAYER),
        position=PositionComponent(GAME_MAP.starting_room.pivot_x, GAME_MAP.starting_room.pivot_y),
        movement=MovementComponent(),
        health=HealthComponent(100),
        tags=TagComponent(['PLAYER']),
        identity=IdentityComponent(name='Player', desc='The player character'),
        inventory=InventoryComponent(size=20),
        collision=CollisionComponent(enabled=True),
        attack=AttackComponent('MELEE'),
        stats=StatComponent()
    )
    random_room = GAME_MAP.get_random_room()

    TEST_MONSTER = Entity(
        sprite=SpriteComponent(Sprites.IMP),
        position=PositionComponent(random_room.pivot_x, random_room.pivot_y),
        movement=MovementComponent(),
        health=HealthComponent(100),
        tags=TagComponent(['LOOTABLE', 'MONSTER']),
        identity=IdentityComponent(name='Monster', desc='Spooky Scary Skeleton'),
        inventory=InventoryComponent(size=20),
        collision=CollisionComponent(enabled=True)
    )

    TEST_ITEM = Entity(
        sprite=SpriteComponent(Sprites.MISSING),
        tags=TagComponent(['EQUIPPABLE']),
        identity=IdentityComponent(name='The Mighty Sword', desc='A powerful sword (+2 DMG)'),
        modifiers=StatModifierComponent({'DAMAGE': 2})
    )
    TEST_ITEM2 = Entity(
        sprite=SpriteComponent(Sprites.MISSING),
        tags=TagComponent(['EQUIPPABLE']),
        identity=IdentityComponent(name='The Mighty Sword', desc='A powerful sword (+2 DMG)'),
        modifiers=StatModifierComponent({'DAMAGE': 2})
    )
    TEST_ITEM3 = Entity(
        sprite=SpriteComponent(Sprites.MISSING),
        tags=TagComponent(['EQUIPPABLE']),
        identity=IdentityComponent(name='The Mighty Sword', desc='A powerful sword (+2 DMG)'),
        modifiers=StatModifierComponent({'DAMAGE': 2})
    )

    PLAYER.inventory.items.update({TEST_ITEM: 1})
    PLAYER.inventory.items.update({TEST_ITEM2: 2})
    PLAYER.inventory.items.update({TEST_ITEM3: 13})
    TEST_ITEM.modifiers.add_modifier({'HEALTH': -2})

    # Move camera to the player
    Globals.CAMERA_CURRENT_X = PLAYER.position.x
    Globals.CAMERA_CURRENT_Y = PLAYER.position.y

    # Add player to entities for looping in systems
    Globals.ENTITIES.append(PLAYER)
    Globals.ENTITIES.append(TEST_MONSTER)
    Globals.ENTITIES.append(TEST_ITEM)
    Globals.ENTITIES.append(TEST_ITEM2)
    Globals.ENTITIES.append(TEST_ITEM3)


def game_main_loop():
    # The main game loop
    clock = pygame.time.Clock()
    running = True
    global FOV_MAP, CURRENT_ACTION_INDEX

    # The Actual Loop
    while running:
        # Get events
        for event in pygame.event.get():
            # [x]/Alt+F4 etc. pressed
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # input_handlers.py -> handle_keys(key, player)
                action = handle_keys(event.key, PLAYER)

                # Result from handle_keys in format {'attribute': value}
                if isinstance(action, MovementAction):
                    action.execute()
                    # Add action to stack so we can undo/redo easily
                    CURRENT_ACTION_INDEX += 1
                    del Globals.ACTIONS[CURRENT_ACTION_INDEX:]
                    Globals.ACTIONS.append(action)
                else:
                    toggle_fov = action.get('fov')
                    toggle_map = action.get('map')
                    gen_map = action.get('generate')
                    undo = action.get('undo')
                    redo = action.get('redo')

                    if gen_map:
                        # Re-generate the map with new seed (DEV)
                        Globals.ENTITIES = [PLAYER]
                        Globals.ENTITIES.extend(GAME_MAP.generate(12))
                        PLAYER.position.x = GAME_MAP.starting_room.pivot_x
                        PLAYER.position.y = GAME_MAP.starting_room.pivot_y
                        Globals.CAMERA_CURRENT_X = PLAYER.position.x
                        Globals.CAMERA_CURRENT_Y = PLAYER.position.y
                        FOV_MAP = fov.initialize_fov(GAME_MAP)
                    if toggle_fov:
                        # Enable/Disable FOV ?(DEV)?
                        Globals.FOV_ENABLED = not Globals.FOV_ENABLED
                    if toggle_map:
                        # Full screen map ?(DEV)?
                        Globals.FULL_MAP = not Globals.FULL_MAP
                    if undo:
                        if len(Globals.ACTIONS) > 0 and CURRENT_ACTION_INDEX >= 0:
                            Globals.ACTIONS[CURRENT_ACTION_INDEX].undo()
                            CURRENT_ACTION_INDEX -= 1
                        else:
                            print("Nothing to undo.")
                    if redo:
                        if CURRENT_ACTION_INDEX < len(Globals.ACTIONS) - 1:
                            CURRENT_ACTION_INDEX += 1
                            Globals.ACTIONS[CURRENT_ACTION_INDEX].redo()
                        else:
                            print("Nothing to redo.")
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_buttons(event.button)

        # If we need to recompute the FOV, e.g. the player has moved (movement_system.py)
        if Globals.FOV_RECOMPUTE:
            fov.recompute_fov(FOV_MAP, PLAYER.position.x, PLAYER.position.y, 5)

        # Update systems
        RENDER_SYSTEM.update(GAME_MAP, FOV_MAP)
        player_movement_success = MOVEMENT_SYSTEM.update(GAME_MAP)
        if not player_movement_success:
            Globals.ACTIONS.pop()
            CURRENT_ACTION_INDEX -= 1

        # Wait until next frame (60 FPS)
        Globals.TICK += 1
        clock.tick(60)

    # If we reach this, pygame.QUIT event has been issued, see above
    pygame.quit()
    exit()


if __name__ == "__main__":
    game_init()
    game_main_loop()
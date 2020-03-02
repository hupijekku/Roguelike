import pygame
import os
pygame.init()


class Constants:
    # Game window variables
    GAME_WIDTH = 1280
    GAME_HEIGHT = 720
    INVENTORY_WIDTH = 320
    INVENTORY_HEIGHT = 580
    LOG_WIDTH = 1280
    LOG_HEIGHT = 180
    MINIMAP_WIDTH = 320
    MINIMAP_HEIGHT = 320

    WINDOW_WIDTH = GAME_WIDTH + INVENTORY_WIDTH
    WINDOW_HEIGHT = GAME_HEIGHT + LOG_HEIGHT

    # Cell variables
    CELL_WIDTH = 16
    CELL_HEIGHT = 16

    # Camera variables, size in Tiles (16px, 16px)
    CAMERA_WIDTH = 16
    CAMERA_HEIGHT = 9

    # Map variables, size in Tiles (16px, 16px)
    MAP_WIDTH = 60
    MAP_HEIGHT = 60


class Globals:

    # Data
    ENTITIES = []
    ACTIONS = []

    # Camera coordinates
    CAMERA_CURRENT_X = int(Constants.CAMERA_WIDTH/2-2)
    CAMERA_CURRENT_Y = int(Constants.CAMERA_HEIGHT/2-2)

    # UUID Counter
    UUID = 0

    # Current tick
    TICK = 0

    # OTHER
    FULL_MAP = False
    FOV_RECOMPUTE = True
    FOV_ENABLED = True


class Sprites:
    PLAYER = pygame.image.load(os.path.join('Images', 'player_idle_0.png'))
    IMP = pygame.image.load(os.path.join('Images', 'imp_idle_0.png'))
    WALL = pygame.image.load(os.path.join('Images', 'wall.png'))
    FLOOR = pygame.image.load(os.path.join('Images', 'floor.png'))
    MISSING = pygame.image.load(os.path.join('Images', 'skull.png'))
    DOOR = pygame.image.load(os.path.join('Images', 'door.png'))
    # TODO: Get new door sprite with correct size or scale it down manually
    DOOR = pygame.transform.scale(DOOR, (16, 16))
    FOV = pygame.image.load(os.path.join('Images', 'black.png'))

    # These have to be initialized in main.py after setting display mode.
    # Could possibly have
    #   import pygame
    #   pygame.display.set_mode(GAME_WIDTH, GAME_HEIGHT)
    # in this script too?
    FOV_OVERLAY = None
    FOV_WALL = None
    FOV_FLOOR = None
    FOV_DOOR = None

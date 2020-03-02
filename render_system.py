import pygame
import tcod
from globals import Sprites
from globals import Constants
from globals import Globals
import log
import utils


def clamp(n, minn, maxn): return min(max(n, minn), maxn)


class RenderSystem:
    def __init__(self, main_window, inventory_surface, minimap_surface, log_surface):
        # Renderer constructor

        # Initialize pygame
        pygame.init()

        # Initialize the game window given as parameter
        self.main_window = main_window
        self.inventory_surface = inventory_surface
        self.minimap_surface = minimap_surface
        self.log_surface = log_surface

        self.game_surface = pygame.Surface((Constants.CELL_WIDTH * Constants.CAMERA_WIDTH,
                                            Constants.CELL_HEIGHT * Constants.CAMERA_HEIGHT))
        self.temp = self.game_surface

    def update(self, game_map, fov_map):

        # Switch map state
        if Globals.FULL_MAP:
            self.game_surface = self.main_window
        else:
            self.game_surface = self.temp

        # Fill the screen (Temporary, just update what moves?)
        self.game_surface.fill((100, 100, 100))

        # Change variables based on current map state
        if Globals.FULL_MAP:
            y1 = 0
            x1 = 0
            y2 = Constants.MAP_HEIGHT
            x2 = Constants.MAP_WIDTH
            render_x = 0
            render_y = 0
        else:
            y1 = Globals.CAMERA_CURRENT_Y - 3
            y2 = Globals.CAMERA_CURRENT_Y + 8
            x1 = Globals.CAMERA_CURRENT_X - 6
            x2 = Globals.CAMERA_CURRENT_X + 10
            render_x = Globals.CAMERA_CURRENT_X - 6
            render_y = Globals.CAMERA_CURRENT_Y - 3

        # Limit ranges to stay inside the map
        y2 = utils.clamp(y2, 0, Constants.MAP_HEIGHT)
        x2 = utils.clamp(x2, 0, Constants.MAP_WIDTH)

        # Loop the map and render sprites based on FOV
        for y in range(y1, y2):
            for x in range(x1, x2):
                if tcod.map_is_in_fov(fov_map, x, y) or not Globals.FOV_ENABLED:
                    if not game_map.is_blocked(x, y):
                        self.game_surface.blit(Sprites.FLOOR,
                                               (Constants.CELL_WIDTH * (x - render_x),
                                                Constants.CELL_HEIGHT * (y - render_y)))
                    else:
                        self.game_surface.blit(Sprites.WALL,
                                               (Constants.CELL_WIDTH * (x - render_x),
                                                Constants.CELL_HEIGHT * (y - render_y)))
                    game_map.tiles[x][y].set_seen(True)
                else:
                    if game_map.tiles[x][y].seen:
                        if not game_map.is_blocked(x, y):
                            self.game_surface.blit(Sprites.FOV_FLOOR,
                                                   (Constants.CELL_WIDTH * (x - render_x),
                                                    Constants.CELL_HEIGHT * (y - render_y)),
                                                   special_flags=pygame.BLEND_RGBA_MULT)
                        else:
                            self.game_surface.blit(Sprites.FOV_WALL,
                                                   (Constants.CELL_WIDTH * (x - render_x),
                                                    Constants.CELL_HEIGHT * (y - render_y)),
                                                   special_flags=pygame.BLEND_RGBA_MULT)
                    else:
                        self.game_surface.blit(Sprites.FOV,
                                               (Constants.CELL_WIDTH * (x - render_x),
                                                Constants.CELL_HEIGHT * (y - render_y)))
        # Render entities
        for entity in Globals.ENTITIES:
            if entity.sprite and entity.position:
                self.draw_entity(entity, game_map, fov_map)

        # Scale the image to fit window and update
        self.draw_minimap(game_map)
        self.draw_log()
        self.draw_inventory()
        if not Globals.FULL_MAP:
            self.game_surface = pygame.transform.scale(self.game_surface, (Constants.GAME_WIDTH, Constants.GAME_HEIGHT))
        self.main_window.blit(self.game_surface, (0, 0))
        self.main_window.blit(self.minimap_surface, (Constants.GAME_WIDTH, 0))
        self.main_window.blit(self.log_surface, (0, Constants.GAME_HEIGHT))
        self.main_window.blit(self.inventory_surface, (Constants.GAME_WIDTH, Constants.MINIMAP_HEIGHT))
        pygame.display.flip()

    def draw_entity(self, entity, game_map, fov_map):
        # Change variables based on map state
        if Globals.FULL_MAP:
            render_x = 0
            render_y = 0
        else:
            render_x = Globals.CAMERA_CURRENT_X - 6
            render_y = Globals.CAMERA_CURRENT_Y - 3
        # Render sprite based on FOV
        if tcod.map_is_in_fov(fov_map, entity.position.x, entity.position.y) or not Globals.FOV_ENABLED:
            self.game_surface.blit(entity.sprite.image,
                                   ((entity.position.x - render_x)
                                    * Constants.CELL_WIDTH + entity.sprite.draw_offset_x,
                                    (entity.position.y - render_y)
                                    * Constants.CELL_HEIGHT + entity.sprite.draw_offset_y))
        elif game_map.tiles[entity.position.x][entity.position.y].seen:
            self.game_surface.blit(entity.sprite.seen,
                                   ((entity.position.x - render_x)
                                    * Constants.CELL_WIDTH + entity.sprite.draw_offset_x,
                                    (entity.position.y - render_y)
                                    * Constants.CELL_HEIGHT + entity.sprite.draw_offset_y),
                                   special_flags=pygame.BLEND_RGBA_MULT)

    def draw_minimap(self, game_map):
        self.minimap_surface.fill((100, 100, 100))
        mini_map = pygame.Surface((Constants.MAP_WIDTH, Constants.MAP_HEIGHT)).convert_alpha()
        px_array = pygame.PixelArray(mini_map)
        player_x = 0
        player_y = 0
        for y in range(Constants.MAP_HEIGHT):
            for x in range(Constants.MAP_WIDTH):
                if game_map.tiles[x][y].seen:
                    if game_map.tiles[x][y].walkable:
                        px_array[x][y] = (100, 100, 100)
                    else:
                        px_array[x][y] = (255, 255, 255)
        for entity in Globals.ENTITIES:
            if entity.tags and 'PLAYER' in entity.tags():
                player_x = entity.position.x
                player_y = entity.position.y
                px_array[player_x][player_y] = (0, 0, 255)
            elif entity.sprite and entity.position:
                if game_map.tiles[entity.position.x][entity.position.y].seen:
                    if entity.tags and 'DOOR' in entity.tags():
                        px_array[entity.position.x][entity.position.y] = (120, 0, 0)
                    else:
                        px_array[entity.position.x][entity.position.y] = (255, 0, 0)
        font = pygame.font.SysFont("consolas", 24)
        text = font.render("{},{}".format(player_x, player_y), True, (200, 200, 200))

        px_array.close()
        pygame.transform.scale(mini_map, (Constants.MINIMAP_WIDTH, Constants.MINIMAP_HEIGHT), self.minimap_surface)
        self.minimap_surface.blit(text, (5, 5))

    def draw_log(self):
        self.log_surface.fill((10, 10, 10))
        font = pygame.font.SysFont("consolas", 18)
        i = 0;
        for message in log.messages[-8:]:
            text = font.render(message.text, True, message.color)
            self.log_surface.blit(text, (5, 20*i+5))
            i += 1

    def draw_inventory(self):
        font_large = pygame.font.SysFont("consolas", 40)
        font_small = pygame.font.SysFont("consolas", 20)
        self.inventory_surface.fill((255, 255, 255))
        text = font_large.render("Inventory", True, (0, 0, 0))
        self.inventory_surface.blit(text, (18, 10))
        for entity in Globals.ENTITIES:
            if entity.inventory and entity.tags and 'PLAYER' in entity.tags():
                items = len(entity.inventory.items) - 1
                for i in range(entity.inventory.size):
                    x = 58*(i % 5)+18
                    y = 58*(int(i/5))+60
                    pygame.draw.rect(self.inventory_surface, (10, 10, 10), (x, y, 52, 52))
                    pygame.draw.rect(self.inventory_surface, (255, 255, 255), (x+2, y+2, 48, 48))
                    if i <= items:
                        self.inventory_surface.blit(list(entity.inventory.items)[i].sprite.image_large, (x+2, y+2))
                        if list(entity.inventory.items.values())[i] > 1:
                            stringy = str(list(entity.inventory.items.values())[i])
                            strleng = len(stringy)
                            text = font_small.render(stringy, True, (0, 0, 0))
                            self.inventory_surface.blit(text, (x + 35 - ((strleng-1)*10), y + 30))


import pygame
from globals import Globals
from actions import MovementAction

# KEYS:
#   Arrow keys: Move
#   M: Change map state
#   Spacebar: Generate a new map
#   F: Toggle FOV


def handle_keys(key, player):
    if key == pygame.K_UP or key == pygame.K_w:
        return MovementAction(player, None, 0, 1)
    elif key == pygame.K_DOWN or key == pygame.K_s:
        return MovementAction(player, None, 2, 1)
    elif key == pygame.K_LEFT or key == pygame.K_a:
        return MovementAction(player, None, 3, 1)
    elif key == pygame.K_RIGHT or key == pygame.K_d:
        return MovementAction(player, None, 1, 1)
    elif key == pygame.K_m:
        return {'map': True}
    elif key == pygame.K_f:
        return {'fov': True}
    elif key == pygame.K_SPACE:
        return {'generate': True}
    elif key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
        print("UNDO")
        return {'undo': True}
    elif key == pygame.K_y and pygame.key.get_mods() & pygame.KMOD_CTRL:
        print("REDO")
        return {'redo': True}
    elif key == pygame.K_h:
        print(Globals.TICK)

    return {}


def handle_mouse_buttons(key):
    if key == 1:
        # Left Mouse Button
        x = int(pygame.mouse.get_pos()[0] / 16)
        y = int(pygame.mouse.get_pos()[1] / 16)
        print("Mouse at {},{}".format(x, y))
    elif key == 2:
        # MMB
        pass
    elif key == 3:
        # Right Mouse Button
        pass
    elif key == 4:
        # Scroll up
        pass
    elif key == 5:
        # Scroll down
        pass

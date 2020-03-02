from globals import Sprites
import pygame


class BaseComponent:
    def __init__(self):
        self.owner = None


class SpriteComponent(BaseComponent):
    def __init__(self, sprite=None, seen=None):
        if sprite:
            self.image = sprite
            self.image_large = pygame.transform.scale(sprite, (48, 48))
            self.draw_offset_x = 16 - sprite.get_width()
            self.draw_offset_y = 16 - sprite.get_height()
            if seen:
                self.seen = seen
            else:
                self.seen = pygame.Surface([16, 16], pygame.SRCALPHA, 32)
                self.seen = self.seen.convert_alpha()
        else:
            self.sprite = Sprites.MISSING
        BaseComponent.__init__(self)

    def __repr__(self):
        return "\n Sprite"


class PositionComponent(BaseComponent):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        BaseComponent.__init__(self)

    def __repr__(self):
        return "\n Position: {},{}".format(self.x, self.y)


class MovementComponent(BaseComponent):
    def __init__(self, dx=0, dy=0):
        self.dx = dx
        self.dy = dy
        BaseComponent.__init__(self)

    def __repr__(self):
        return "\n Movement: ({},{})".format(self.dx, self.dy)


class HealthComponent(BaseComponent):
    def __init__(self, max_health=10):
        self.max_health = max_health
        self.current_health = max_health
        BaseComponent.__init__(self)

    def __repr__(self):
        return "\n Health: {}/{}".format(self.current_health, self.max_health)


class IdentityComponent(BaseComponent):
    def __init__(self, name='', desc=''):
        self.name = name
        self.desc = desc
        BaseComponent.__init__(self)

    def __repr__(self):
        return "\n Identity: \n  -Name: {}\n  -Desc: {}".format(self.name, self.desc)


class AiComponent(BaseComponent):
    def __init__(self, enable=True):
        self.enabled = enable
        BaseComponent.__init__(self)

    def __repr__(self):
        return "\n AI"


class TagComponent(BaseComponent):
    def __init__(self, tags=None):
        self.tags = []
        if type(tags) is list:
            self.tags.extend(tags)
        BaseComponent.__init__(self)

    def __call__(self, *args, **kwargs):
        return self.tags

    def __repr__(self):
        return "\n Tags: {}".format(self.tags)

    def add_tag(self, tag):
        self.tags.append(tag)

    def remove_tag(self, tag):
        self.tags.remove(tag)


class InventoryComponent(BaseComponent):
    def __init__(self, size):
        self.items = {}
        self.size = size
        BaseComponent.__init__(self)

    def __repr__(self):
        output = "Items: "
        for item in self.items:
            output += "\n " + str(item)
        return output


class StatModifierComponent(BaseComponent):
    def __init__(self, modifier=None):
        if modifier:
            self.modifiers = modifier
        else:
            self.modifiers = {}
        BaseComponent.__init__(self)

    def add_modifier(self, modifier):
        self.modifiers.update(modifier)

    def __repr__(self):
        return "\n Modifiers: {}".format(self.modifiers)


class CollisionComponent(BaseComponent):
    def __init__(self, enabled=True):
        self.enabled = enabled
        BaseComponent.__init__(self)

    def __repr__(self):
        return "Collision: {}".format(self.enabled)


class AttackComponent(BaseComponent):
    def __init__(self, attack_type='MELEE'):
        self.attack_type = attack_type
        BaseComponent.__init__(self)

    def __repr__(self):
        return "Attack Type: {}".format(self.attack_type)


class StatComponent(BaseComponent):
    def __init__(self, strength=5, agility=5, intelligence=5):
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence

    def __repr__(self):
        return """ Stats:
        STR: {}
        AGI: {}
        INT: {}
        """.format(self.strength, self.agility, self.intelligence)
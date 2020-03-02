import pygame
from globals import Globals


class Entity:
    def __init__(self,
                 sprite=None,
                 position=None,
                 movement=None,
                 identity=None,
                 ai=None,
                 tags=None,
                 inventory=None,
                 modifiers=None,
                 health=None,
                 collision=None,
                 attack=None,
                 stats=None
                 ):
        Globals.UUID += 1
        self.entity_id = Globals.UUID
        self.components = []

        if sprite:
            self.sprite = sprite
            sprite.owner = self
            self.components.append(sprite)
        else:
            self.sprite = False

        if position:
            self.position = position
            position.owner = self
            self.components.append(position)
        else:
            self.position = False

        if movement:
            self.movement = movement
            movement.owner = self
            self.components.append(movement)
        else:
            self.movement = False

        if identity:
            self.identity = identity
            identity.owner = self
            self.components.append(identity)
        else:
            self.identity = False

        if ai:
            self.ai = ai
            ai.owner = self
            self.components.append(ai)
        else:
            self.ai = False

        if tags:
            self.tags = tags
            tags.owner = self
            self.components.append(tags)
        else:
            self.tags = False

        if inventory:
            self.inventory = inventory
            inventory.owner = self
            self.components.append(inventory)
        else:
            self.inventory = False

        if modifiers:
            self.modifiers = modifiers
            modifiers.owner = self
            self.components.append(modifiers)
        else:
            self.modifiers = False

        if health:
            self.health = health
            health.owner = self
            self.components.append(health)
        else:
            self.health = False
            
        if collision:
            self.collision = collision
            collision.owner = self
            self.components.append(collision)
        else:
            self.collision = False
            
        if attack:
            self.attack = attack
            attack.owner = self
            self.components.append(attack)
        else:
            self.attack = False

        if stats:
            self.stats = stats
            stats.owner = self
            self.components.append(stats)
        else:
            self.stats = False

    def __repr__(self):
        return "\n<\nEntity id={} components={} \n>\n".format(self.entity_id, self.components)

    def __str__(self):
        if self.identity:
            return "<Entity name={}>".format(self.identity.name)
        else:
            return repr(self)

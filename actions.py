import utils

class BaseAction:

    def __init__(self, origin, target):
        self.origin = origin
        self.target = target
        pass

    def execute(self):
        pass

    def undo(self):
        pass

    def redo(self):
        pass


class MovementAction(BaseAction):

    def __init__(self, origin, target, direction, amount):
        self.direction = direction
        self.amount = amount
        self.target = target
        self.origin = origin
        self.last_move = None
        BaseAction.__init__(self, origin, target)

    def execute(self):
        if self.origin and not self.target:
            if self.origin.position and self.origin.movement:
                movement = {
                    0: (0, -1),
                    1: (1, 0),
                    2: (0, 1),
                    3: (-1, 0)
                }.get(self.direction, (0, 0))
                self.last_move = tuple(i * self.amount for i in movement)
                dx, dy = self.last_move
                self.origin.movement.dx = dx
                self.origin.movement.dy = dy

    def undo(self):
        if self.last_move:
            if self.origin and not self.target:
                if self.origin.position and self.origin.movement:
                    dx, dy = self.last_move
                    self.origin.movement.dx = int(dx*(-1))
                    self.origin.movement.dy = int(dy*(-1))

    def redo(self):
        if self.last_move:
            if self.origin and not self.target:
                if self.origin.position and self.origin.movement:
                    dx, dy = self.last_move
                    self.origin.movement.dx = dx
                    self.origin.movement.dy = dy

    def __repr__(self):
        movement = {
            0: "up",
            1: "right",
            2: "down",
            3: "left"
        }.get(self.direction, (0, 0))
        return movement


class MeleeAttackAction(BaseAction):

    def __init__(self, origin, target, damage):
        self.origin = origin
        self.target = target
        self.damage = damage
        BaseAction.__init__(self, origin, target)

    def execute(self):
        if self.origin.attack and self.target.health:
            self.target.health.current_health = \
                utils.clamp(self.target.health.current_health - self.damage, 0, self.target.health.max_health)

    def undo(self):
        if self.origin.attack and self.target.health:
            self.target.health.current_health = \
                utils.clamp(self.target.health.current_health + self.damage, 0, self.target.health.max_health)

    def redo(self):
        self.execute()

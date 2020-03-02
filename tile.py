class Tile:
    def __init__(self, walkable, transparent):
        self.walkable = walkable
        self.transparent = transparent
        self.seen = False

    def set_seen(self, seen):
        self.seen = seen

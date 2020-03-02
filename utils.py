from globals import Globals

def get_entity_at(x, y):
    for entity in Globals.ENTITIES:
        if entity.position:
            if entity.position.x == x and entity.position.y == y:
                return entity
    return False


def clamp(n, minn, maxn): return min(max(n, minn), maxn)

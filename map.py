from tile import Tile
from entity import Entity
from components import *
import random
import tcod
import numpy


class Map:

    def __init__(self, map_width, map_height):
        self.width = map_width
        self.height = map_height
        self.tiles = self.initialize_tiles()
        self.extra_paths = 12
        self.starting_room = None
        self.rooms = []

    def initialize_tiles(self):
        # Reset map => All tiles WALL
        tiles = [[Tile(False, False) for y in range(self.height)] for x in range(self.width)]
        return tiles

    def is_blocked(self, x, y):
        # Kinda useless function, as you can just check tile.walkable?
        if self.tiles[x][y].walkable:
            return False
        return True

    def generate(self, room_count):
        """ This method procedurally generates a new dungeon
            METHOD:
                    1. Create $room_count of rooms of size randint(4, 7)
                    2. From every room, create path to the next room
                    3. Add extra paths between random rooms to have less far-away dead ends
                    4. Create doors to paths that are not straight lines, and where both sides are walls
         """
        print("")
        print("")
        print("STARTING MAP GENERATION")
        print("#########################")
        # Reset the tiles
        self.tiles = self.initialize_tiles()
        self.extra_paths = 12
        rooms = []
        entities = []

        # Create rooms
        iter = 0
        while iter < room_count:
            x = random.randint(7, self.width - 6)
            y = random.randint(7, self.height - 6)
            w = random.randint(4, 9)
            h = random.randint(4, 9)
            if len(rooms) == 0:
                room = Room(x, y, w, h)
                self._generate_room(room)
                rooms.append(room)
                print("Created room at: {},{} w:{} h:{}".format(x, y, w, h))
            else:
                valid = True
                for room in rooms:
                    if room.is_in_room(x, y, w, h):
                        valid = False
                if valid:
                    print(iter)
                    room = Room(x, y, w, h)
                    self._generate_room(room)
                    rooms.append(room)
                    print("Created room at: {},{} w:{} h:{}".format(x, y, w, h))
                else:
                    print("Roomcount++")
                    room_count += 1
            # print("{}, {}".format(iter, room_count))
            iter += 1
        # From every room (except last), create a pathway to the next room
        for i in range(len(rooms) - 1):
            self._generate_path_test(rooms[i].pivot_x, rooms[i].pivot_y, rooms[i + 1].pivot_x, rooms[i + 1].pivot_y)
            rooms[i].path_y = True
            rooms[i + 1].path_x = True
        self._generate_path_test(rooms[0].pivot_x, rooms[0].pivot_y, rooms[len(rooms)-1].pivot_x, rooms[len(rooms)-1].pivot_y)
        # paths = self.extra_paths
        # # Create extra paths to remove dead ends
        # for j in range(0, paths):
        #     a = random.randint(0, len(rooms) - 1)
        #     b = random.randint(0, len(rooms) - 1)
        #     # If indexes are same or next to each other, there is already a pathway between them
        #     if b - a <= 1:
        #         if self._generate_path_test(rooms[a].pivot_x, rooms[a].pivot_y, rooms[b].pivot_x, rooms[b].pivot_y):
        #             rooms[a].path_y = True
        #             rooms[b].path_x = True
        # Set the starting room and return the door entities for main.py=>ENTITIES
        for k in range(len(rooms) - 1):
            if rooms[k].path_x or rooms[k].path_y:
                self.starting_room = rooms[k]

            entities.extend(rooms[k].create_doors(self.tiles))
        door_x = False
        door_y = False
        door_y_prev = False
        for y in range(self.height):
            if door_y_prev:
                door_y = True
                door_y_prev = False
            door_x = False
            for x in range(self.width):
                if self.tiles[x][y].walkable:
                    if not self.tiles[x-1][y].walkable and not self.tiles[x+1][y].walkable:
                        if random.randint(1, 100) < 15 and not door_y:
                            entities.append(Entity(
                                sprite=SpriteComponent(Sprites.DOOR, Sprites.FOV_DOOR),
                                position=PositionComponent(x, y),
                                tags=TagComponent(['DOOR']),
                                identity=IdentityComponent(name='Door', desc='A sturdy wooden door')
                            ))
                            print("CREATED AN EXTRA DOOR AT {},{}".format(x, y))
                            door_y_prev = True
                            door_y = False
                    if not self.tiles[x][y-1].walkable and not self.tiles[x][y+1].walkable:
                        if random.randint(1, 100) < 15 and not door_x:
                            entities.append(Entity(
                                sprite=SpriteComponent(Sprites.DOOR, Sprites.FOV_DOOR),
                                position=PositionComponent(x, y),
                                tags=TagComponent(['DOOR']),
                                identity=IdentityComponent(name='Door', desc='A sturdy wooden door')
                            ))
                            print("CREATED AN EXTRA DOOR AT {},{}".format(x, y))
                            door_x = True

        self.rooms = rooms
        return entities

    def _generate_path(self, start_x, start_y, end_x, end_y):
        if int(abs(start_x - end_x) + abs(start_y - end_y)) > 70:
            self.extra_paths += 1
            return False
        if start_y > end_y:
            for y in range(end_y, start_y + 1):
                self.tiles[start_x][y].walkable = True
                self.tiles[start_x][y].transparent = True
        else:
            for y in range(start_y, end_y + 1):
                self.tiles[start_x][y].walkable = True
                self.tiles[start_x][y].transparent = True
        if start_x > end_x:
            for x in range(end_x, start_x):
                self.tiles[x][end_y].walkable = True
                self.tiles[x][end_y].transparent = True
        else:
            for x in range(start_x, end_x):
                self.tiles[x][end_y].walkable = True
                self.tiles[x][end_y].transparent = True
        print("Created path from {},{} to {},{}".format(start_x, start_y, end_x, end_y))
        return True

    def _generate_path_test(self, s_x, s_y, e_x, e_y):
        noise = tcod.noise.Noise(2)
        noise_map = [[1 + noise.get_point(x, y) for y in range(self.height)] for x in range(self.width)]
        a_star = tcod.path.AStar(numpy.array(noise_map, dtype=numpy.float32), 0)
        path = a_star.get_path(s_x, s_y, e_x, e_y)

        for cords in path:
            x, y = cords
            self.tiles[x][y].walkable = True
            self.tiles[x][y].transparent = True

    def _generate_room(self, room):
        start_x = int(room.pivot_x - (room.width / 2))
        start_y = int(room.pivot_y - (room.height / 2))
        for y in range(start_y, start_y + room.height):
            for x in range(start_x, start_x + room.width):
                self.tiles[x][y].walkable = True
                self.tiles[x][y].transparent = True
        pass

    def get_random_room(self):
        i = random.randint(0, len(self.rooms) - 1)
        return self.rooms[i]


class Room:

    def __init__(self, pivot_x, pivot_y, width, height):
        self.pivot_x = pivot_x
        self.pivot_y = pivot_y
        self.width = width
        self.height = height
        self.path_y = False
        self.path_x = False
        pass

    def create_doors(self, tiles):
        doors = []
        x = self.pivot_x
        y = self.pivot_y
        if self.path_x:
            for i in range(int(x - (self.width / 2) - 1), int(x + (self.width / 2) + 1)):
                if not tiles[i][y + 1].walkable and not tiles[i][y - 1].walkable and tiles[i][y].walkable:
                    print("Created door at: {},{}".format(i, y))
                    tiles[i][y].transparent = False
                    doors.append(Entity(
                        sprite=SpriteComponent(Sprites.DOOR, Sprites.FOV_DOOR),
                        position=PositionComponent(i, y),
                        tags=TagComponent(['DOOR']),
                        identity=IdentityComponent(name='Door', desc='A sturdy wooden door')
                    ))
        if self.path_y:
            for j in range(int(y - (self.height / 2) - 1), int(y + (self.height / 2) + 1)):
                if not tiles[x + 1][j].walkable and not tiles[x - 1][j].walkable and tiles[x][j].walkable:
                    print("Created door at: {},{}".format(x, j))
                    tiles[x][j].transparent = False
                    doors.append(Entity(
                        sprite=SpriteComponent(Sprites.DOOR, Sprites.FOV_DOOR),
                        position=PositionComponent(x, j),
                        tags=TagComponent(['DOOR']),
                        identity=IdentityComponent(name='Door', desc='A sturdy wooden door')
                    ))
        return doors

    def is_in_room(self, x, y, w, h):
        if self.pivot_x - int(self.width / 2) - w < x < self.pivot_x + int(self.width / 2) + w and \
                self.pivot_y - int(self.height / 2) - h < y < self.pivot_y + int(self.height / 2) + h:
            return True
        print("{},{}  w{} h{}, {},{}".format(self.pivot_x, self.pivot_y, self.width, self.height, x, y))
        return False

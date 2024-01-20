import pygame
from Scripts.GameObject.game_object import GameObject
from typing import List
import random
import math
import json
from Scripts.sprite import PNGSprite
from collections import defaultdict
from pydantic import BaseModel


class PointOfInterest(BaseModel):
    name: str
    sprite_sheet: str
    size: List[int]


class Biome(BaseModel):
    name: str
    tile_set: str
    points_of_interest: List[str]
    environment_objects: List[str]


class WorldGeneration:
    TILE_SIZE = 32

    def __init__(self):
        self.ground = self.make_background(60, 50)
        self.right_border = self.ground.get_rect().right
        self.bot_border = self.ground.get_rect().bottom
        self.tile_map = [
            ([0] * (self.right_border // 32)) for i in range(self.bot_border // 32)
        ]
        self.placed_tiles = defaultdict(list)
        self.game_objects: List[GameObject] = []
        self.active_biomes = []

        for name in ["forest", "planes"]:
            with open(f"GameData/Biomes/{name}.json", "r") as file:
                biome_data = json.load(file)
            self.active_biomes.append(Biome(**biome_data))

        self.generate_biomes(self.active_biomes)

        self.generate_pois(num_of_pois=5)

        self.generate_paths(4)

        for i in range(100):
            _pos = (
                random.randrange(0, self.ground.get_rect().right),
                random.randrange(0, self.ground.get_rect().bottom),
            )
            sprite_sheet = pygame.image.load("Sprites/Tree.png").convert_alpha()
            sprite = PNGSprite().make_from_sprite_sheet(sprite_sheet, 20, 40)
            self.game_objects.append(GameObject(_pos, sprite))

    # TODO
    # 4. place crossroad nodes inside a box defined by the poi's
    # 5. build path network from tree made out of crossroads and poi's
    # 6. place environment filler based on density's defined by biome

    def make_background(self, width: int, height: int) -> pygame.Surface:
        return pygame.Surface(
            size=(width * WorldGeneration.TILE_SIZE, height * WorldGeneration.TILE_SIZE)
        )

    def generate_biomes(self, active_biomes: List[Biome]):
        for biome in active_biomes:
            _pos = (
                random.randrange(0, self.right_border // 32),
                random.randrange(0, self.bot_border // 32),
            )
            while self.tile_map[_pos[1]][_pos[0]] != 0:
                _pos = (
                    random.randrange(0, self.right_border // 32),
                    random.randrange(0, self.bot_border // 32),
                )
            image = pygame.image.load(biome.tile_set)
            self.ground.blit(
                image, tuple([WorldGeneration.TILE_SIZE * cord for cord in _pos])
            )
            self.placed_tiles[biome.name].append(_pos)
            self.tile_map[_pos[1]][_pos[0]] = biome.name

        num_tiles_to_place = ((self.right_border // WorldGeneration.TILE_SIZE) * (self.bot_border // WorldGeneration.TILE_SIZE)) - 2
        tiles_placed = 0
        while tiles_placed < num_tiles_to_place:
            for biome in active_biomes:
                for tile_pos in self.placed_tiles[biome.name]:
                    zero_neighbors = self.get_zero_neighbor(
                        tile_map=self.tile_map, position=tile_pos
                    )
                    if len(zero_neighbors) == 0:
                        continue
                    rand_tile_pos = zero_neighbors[
                        random.randrange(0, len(zero_neighbors))
                    ]

                    image = pygame.image.load(biome.tile_set)
                    self.ground.blit(
                        image,
                        tuple([WorldGeneration.TILE_SIZE * cord for cord in rand_tile_pos])
                    )
                    tiles_placed += 1
                    self.placed_tiles[biome.name].append(rand_tile_pos)
                    self.tile_map[rand_tile_pos[1]][rand_tile_pos[0]] = biome.name
                    break
        print("tiles Placed ", tiles_placed)
        print(num_tiles_to_place + 2)

    def get_zero_neighbor(self, tile_map, position):
        out = []
        for i in [-1, 0, 1]:
            if position[1] + i >= self.bot_border // WorldGeneration.TILE_SIZE:
                continue
            if position[1] + i < 0:
                continue
            for j in [-1, 0, 1]:
                if position[0] + j < 0:
                    continue
                if position[0] + j >= self.right_border // WorldGeneration.TILE_SIZE:
                    continue
                if tile_map[position[1] + i][position[0] + j] == 0:
                    out.append((position[0] + j, position[1] + i))
        return out

    def generate_pois(self, num_of_pois: int):
        for i in range(num_of_pois):
            _pos = (
                random.randrange(0, (self.right_border // 32)),
                random.randrange(0, (self.bot_border // 32)-1),
            )
            for biome in self.active_biomes:
                if biome.name == self.tile_map[_pos[1]][_pos[0]]:
                    cur_biome = biome
                    print(cur_biome)
                    break

            poi_name = cur_biome.points_of_interest[
                random.randrange(len(cur_biome.points_of_interest))
            ]

            with open(f"GameData/PointsOfInterest/{poi_name}.json", "r") as file:
                poi_data = json.load(file)

            poi = PointOfInterest(**poi_data)

            if (
                _pos[0] + poi.size[0] > self.right_border | _pos[1] + poi.size[1] > self.bot_border-1
            ):
                i -= 1
                continue
            if _pos[1] + poi.size[1] > self.bot_border:
                i -= 1
                continue

            sprite_sheet = pygame.image.load(poi.sprite_sheet).convert_alpha()
            sprite = PNGSprite().make_from_sprite_sheet(
                sprite_sheet,
                poi.size[0] * WorldGeneration.TILE_SIZE,
                poi.size[1] * WorldGeneration.TILE_SIZE,
            )
            self.game_objects.append(
                GameObject(
                    tuple([WorldGeneration.TILE_SIZE * cord for cord in _pos]),
                    sprite,
                    "poi",
                )
            )

    def generate_paths(self, num_crossroads: int):
        crossroads = self.generate_crossroads(num_crossroads=num_crossroads)
        pois = []
        for o in self.game_objects:
            if o.tag == "poi":
                pois.append(pygame.Vector2(o.position) // WorldGeneration.TILE_SIZE)
        nodes = [[pygame.Vector2(pos), "crossroad"] for pos in crossroads]
        nodes.extend([[x, "poi"] for x in pois])
        nodes = [[i, node] for i, node in enumerate(nodes)]

        edges = self.generate_min_span_tree(nodes)
        print(edges)
        self.draw_paths(edges, nodes)

    def generate_crossroads(self, num_crossroads: int):
        top_most_poi_cord = self.bot_border
        bot_most_poi_cord = 0
        left_most_poi_cord = self.right_border
        right_most_poi_cord = 0
        crossroad_positions = []
        for game_object in self.game_objects:
            if game_object.tag == "poi":
                top_most_poi_cord = min(top_most_poi_cord, game_object.position[1])
                bot_most_poi_cord = max(bot_most_poi_cord, game_object.position[1])
                left_most_poi_cord = min(left_most_poi_cord, game_object.position[0])
                right_most_poi_cord = max(right_most_poi_cord, game_object.position[0])
        for i in range(num_crossroads):
            _pos = (
                random.randrange(left_most_poi_cord, right_most_poi_cord),
                random.randrange(top_most_poi_cord, bot_most_poi_cord),
            )
            crossroad_positions.append(
                [cord // WorldGeneration.TILE_SIZE for cord in _pos]
            )
        return crossroad_positions

    def generate_min_span_tree(self, nodes: list):
        nodes = [[x[0], x[1][0]] for x in nodes]
        # Kruskalls algo
        dist_list = []

        for source in nodes:
            for dest in nodes:
                if source[0] >= dest[0]:
                    continue
                s_to_d = dest[1] - source[1]
                dist = math.sqrt(s_to_d[0] ** 2 + s_to_d[1] ** 2)
                dist_list.append([[source[0], dest[0]], [source[1], dest[1]], dist])

        dist_list = sorted(dist_list, key=lambda x: x[2])

        active_edges = []
        connected_verts = [{x[0]} for x in nodes]
        while len((active_edges)) < len(nodes) - 1:
            edge = dist_list[0][0]

            is_cycle = self.check_cycle(edge, connected_verts)
            if is_cycle:
                dist_list.pop(0)
                continue

            too_many_incident = self.check_incident(edge=edge, edges=active_edges)
            if too_many_incident:
                dist_list.pop(0)
                continue

            active_edges.append(dist_list[0])
            set_1 = None
            set_2 = None
            for vert_set in connected_verts:
                if set_1 == None:
                    if edge[0] in vert_set:
                        set_1 = vert_set
                    if edge[1] in vert_set:
                        set_1 = vert_set
                else:
                    if edge[0] in vert_set:
                        set_2 = vert_set
                        break
                    if edge[1] in vert_set:
                        set_2 = vert_set
                        break

            connected_verts.append(set_1.union(set_2))
            connected_verts.remove(set_1)
            connected_verts.remove(set_2)
            dist_list.pop(0)
        print(active_edges)
        return active_edges
    def check_cycle(self, edge, connected_verts):
        for vert_set in connected_verts:
            if edge[0] in vert_set and edge[1] in vert_set:
                return True
        return False

    def check_incident(self, edge, edges):
        for vert in edge:
            verts_incident = 0
            for _edge in edges:
                if vert in _edge:
                    verts_incident += 1
            if verts_incident > 4:
                return True
        return False
    
    def draw_paths(self, edges, nodes):
        print(nodes)
        for edge in edges:
            src = edge[1][0] + pygame.Vector2(0, 1)
            dest = edge[1][1] +  pygame.Vector2(0, 1)

            pos = src
            direction = pygame.Vector2(0, 0)
            while pos != dest:
                if pos[1] - dest[1] < 0:
                    next_pos = pos + [0, 1]
                elif pos[1] - dest[1] > 0:
                    next_pos = pos - [0, 1]
                elif pos[0] - dest[0] < 0:
                    next_pos = pos + [1, 0]
                elif pos[0] - dest[0] > 0:
                    next_pos = pos - [1, 0]
                
                next_direction = next_pos - pos
                if next_direction != direction:
                    image = pygame.image.load("Sprites/PathTiles/2way.png")
                    path_direction = tuple(next_direction + direction)
                    match path_direction:
                        case (1, 1):
                            image = pygame.transform.flip(image, flip_x=False, flip_y=True)
                        case (1, -1):
                            image = pygame.transform.flip(image, flip_x=False, flip_y=False)
                        case (-1, 1):
                            image = pygame.transform.flip(image, flip_x=True, flip_y=True)
                        case (-1, -1):
                            image = pygame.transform.flip(image, flip_x=True, flip_y=False)
                        case (1, 0):
                            image = pygame.transform.flip(image, flip_x=False, flip_y=True)
                        case (-1, 0):
                            image = pygame.transform.flip(image, flip_x=True, flip_y=True)
                        case (0, 1):
                            image = pygame.image.load("Sprites/PathTiles/straight.png")
                        case (0, -1):
                            image = pygame.image.load("Sprites/PathTiles/straight.png")
                else:
                    image = pygame.image.load("Sprites/PathTiles/straight.png")
                    if direction[1] == 0:
                        image = pygame.transform.rotate(image, 90)
                
                self.ground.blit(image, pos*WorldGeneration.TILE_SIZE)
                pos = next_pos
                direction = next_direction
            dest_node = nodes[edge[0][1]]
            if dest_node[1][1] == "poi":
                print(direction)
                match tuple(direction):
                    case (1, 0):
                        image = pygame.image.load("Sprites/PathTiles/2way.png")
                        image = pygame.transform.flip(image, flip_x=True, flip_y=True)
                    case (0, 1):
                        image = pygame.image.load("Sprites/PathTiles/straight.png")
                    case (-1, 0):
                        image = pygame.image.load("Sprites/PathTiles/2way.png")
                        image = pygame.transform.flip(image, flip_x=False, flip_y=True)
                    case (0, -1):
                        image = pygame.image.load("Sprites/PathTiles/straight.png")
            

            self.ground.blit(image, pos*WorldGeneration.TILE_SIZE)


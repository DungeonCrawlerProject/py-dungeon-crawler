import pygame
from Scripts.GameObject.game_object import GameObject
from typing import List, Dict, Tuple
import random
import math

from Scripts.WorldGeneration.biome import Biome
from Scripts.WorldGeneration.point_of_interest import PointOfInterest
from Scripts.Enemy.enemy_handler import EnemyHandler
from Scripts.sprite import PNGSprite
from collections import defaultdict

import numpy as np
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise


class WorldGeneration:
    TILE_SIZE = 32

    def __init__(self, enemy_handler: EnemyHandler):
        self.enemy_handler = enemy_handler
        self.noise_map = None
        self.ground = self.make_background(256, 128)
        self.right_border = self.ground.get_rect().right
        self.bot_border = self.ground.get_rect().bottom
        self.tile_map = [
            ([0] * (self.right_border // 32)) for _ in range(self.bot_border // 32)
        ]
        self.placed_tiles = defaultdict(list)
        self.game_objects: List[GameObject] = []

        self.active_biomes = {
            "forest": Biome.from_json("GameData/Biomes/forest.json"),
            "mountain_hills": Biome.from_json("GameData/Biomes/mountain_hills.json"),
            "planes": Biome.from_json("GameData/Biomes/planes.json"),
            "taiga": Biome.from_json("GameData/Biomes/taiga.json"),
            "tundra": Biome.from_json("GameData/Biomes/tundra.json"),
            "ocean": Biome.from_json("GameData/Biomes/ocean.json"),
        }

        self.generate_biomes(self.active_biomes)

        self.generate_pois(num_of_pois=100)
        self.game_objects.extend(self.enemy_handler.active_enemys)

        self.generate_paths(16)

        for i in range(1000):
            _pos = (
                random.randrange(0, self.ground.get_rect().right),
                random.randrange(0, self.ground.get_rect().bottom),
            )

            if self.set_biome_by_intensity(self.noise_map[_pos[1]//self.TILE_SIZE][_pos[0]//self.TILE_SIZE], self.active_biomes) != self.active_biomes["forest"]:
                continue
            self.game_objects.append(GameObject(_pos, PNGSprite().make_single_sprite("Sprites/Tree.png")))

    # TODO
    # 4. place crossroad nodes inside a box defined by the poi's
    # 5. build path network from tree made out of crossroads and poi's
    # 6. place environment filler based on density's defined by biome

    @staticmethod
    def make_background(width: int, height: int) -> pygame.Surface:
        return pygame.Surface(
            size=(width * WorldGeneration.TILE_SIZE, height * WorldGeneration.TILE_SIZE)
        )

    def generate_biomes(self, biome_types: Dict[str, Biome]) -> None:

        # Generate Perlin noise
        perlin_noise = self.generate_perlin_noise(256, 128, octaves=3, is_debug=False)
        self.noise_map = perlin_noise

        x_size, y_size = perlin_noise.shape
        for _x in range(x_size):
            for _y in range(y_size):
                intensity = perlin_noise[_x][_y]
                biome = self.set_biome_by_intensity(intensity, biome_types)
                self.make_biome_at_coordinate((_y, _x), biome)

    def make_biome_at_coordinate(
            self,
            coordinate: Tuple[int | float, int | float],
            biome: Biome
    ) -> None:
        """
        Makes a biome of the specified type at the coordinate (GLOBAL)
        :param coordinate: The coordinate of the biome referenced from top left
        :param biome: The type of biome to make
        """

        image = pygame.image.load(biome.tile_set)

        self.ground.blit(
            image,
            tuple([WorldGeneration.TILE_SIZE * cord for cord in coordinate])
        )

        self.placed_tiles[biome.name].append(coordinate)
        _x, _y = coordinate
        self.tile_map[_y][_x] = biome.name

    def generate_pois(self, num_of_pois: int) -> None:
        """
        Generates the points of interests
        :param num_of_pois: The number to be generated
        """

        for i in range(num_of_pois):
            _pos = (
                random.randrange(0, (self.right_border // 32)),
                random.randrange(0, (self.bot_border // 32) - 1),
            )

            cur_biome = self.set_biome_by_intensity(self.noise_map[_pos[1]][_pos[0]], self.active_biomes)

            if not cur_biome.points_of_interest:
                continue

            poi_name = cur_biome.points_of_interest[
                random.randrange(len(cur_biome.points_of_interest))
            ]

            poi = PointOfInterest.from_json(f"GameData/PointsOfInterest/{poi_name}.json")

            if _pos[0] + poi.size[0] > self.right_border:
                i -= 1
                continue
            if _pos[1] + poi.size[1] > self.bot_border - 1:
                i -= 1
                continue
            if _pos[1] + poi.size[1] > self.bot_border:
                i -= 1
                continue

            sprite = PNGSprite.make_from_sprite_sheet(
                location=poi.sprite_sheet,
                width=poi.size[0] * WorldGeneration.TILE_SIZE,
                height=poi.size[1] * WorldGeneration.TILE_SIZE,
            )

            position = pygame.Vector2(*_pos) * WorldGeneration.TILE_SIZE

            poi.spawn_enemys(pos=position, enemy_handler=self.enemy_handler)

            self.game_objects.append(
                GameObject(
                    position=position,
                    sprite=sprite,
                    tag="poi",
                )
            )

    def generate_paths(self, num_crossroads: int) -> None:
        """
        Generates the paths between the nodes
        :param num_crossroads: The number of cross roads to use
        """

        crossroads = self.generate_crossroads(num_crossroads=num_crossroads)
        pois = [pygame.Vector2(o.position) // WorldGeneration.TILE_SIZE for o in self.game_objects if o.tag == "poi"]

        nodes = [[pygame.Vector2(pos), "crossroad"] for pos in crossroads]
        nodes.extend([[x, "poi"] for x in pois])
        nodes = [[i, node] for i, node in enumerate(nodes)]

        edges = self.generate_min_span_tree(nodes)
        self.draw_paths(edges, nodes)

    def generate_crossroads(self, num_crossroads: int):
        top_most_poi_cord = self.bot_border
        bot_most_poi_cord = 0
        left_most_poi_cord = self.right_border
        right_most_poi_cord = 0
        crossroad_positions = []
        for game_object in self.game_objects:
            if game_object.tag != "poi":
                continue

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

        # Kruskall's algorithm
        dist_list = []

        for source in nodes:
            for destination in nodes:
                if source[0] >= destination[0]:
                    continue
                s_to_d = destination[1] - source[1]
                dist = math.sqrt(s_to_d[0] ** 2 + s_to_d[1] ** 2)
                dist_list.append([[source[0], destination[0]], [source[1], destination[1]], dist])

        dist_list = sorted(dist_list, key=lambda x: x[2])

        active_edges = []
        connected_vertices = [{x[0]} for x in nodes]
        while len(active_edges) < len(nodes) - 1:
            edge = dist_list[0][0]

            is_cycle = self.check_cycle(edge, connected_vertices)
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
            for vert_set in connected_vertices:
                if set_1 is None:
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

            connected_vertices.append(set_1.union(set_2))
            connected_vertices.remove(set_1)
            connected_vertices.remove(set_2)
            dist_list.pop(0)
        return active_edges

    @staticmethod
    def set_biome_by_intensity(
            val: float,
            biome_dict: Dict[str, Biome]
    ) -> Biome:
        """
        Sets the biome type based on the perlin noises value
        :param val: A value between [-0.5, 0.5]
        :param biome_dict: The dictionary containing the biome information
        :return: The Biome type
        """

        if 0.25 > val >= 0:
            return biome_dict["forest"]
        elif 0.35 > val >= 0.25:
            return biome_dict["taiga"]
        elif val >= 0.45:
            return biome_dict["tundra"]
        elif 0.45 > val >= 0.35:
            return biome_dict["mountain_hills"]
        elif -0.4 <= val < 0:
            return biome_dict["planes"]
        elif val < -0.4:
            return biome_dict["ocean"]

    @staticmethod
    def check_cycle(edge, connected_vertices):
        for vert_set in connected_vertices:
            if edge[0] in vert_set and edge[1] in vert_set:
                return True
        return False

    @staticmethod
    def check_incident(edge, edges):
        for vert in edge:
            vertices_incident = 0
            for _edge in edges:
                if vert in _edge:
                    vertices_incident += 1
            if vertices_incident > 4:
                return True
        return False

    def draw_paths(self, edges, nodes):
        for edge in edges:
            src = edge[1][0] + pygame.Vector2(0, 1)
            destination = edge[1][1] + pygame.Vector2(0, 1)

            image = None

            pos = src
            direction = pygame.Vector2(0, 0)
            while pos != destination:
                if pos[1] - destination[1] < 0:
                    next_pos = pos + [0, 1]
                elif pos[1] - destination[1] > 0:
                    next_pos = pos - [0, 1]
                elif pos[0] - destination[0] < 0:
                    next_pos = pos + [1, 0]
                elif pos[0] - destination[0] > 0:
                    next_pos = pos - [1, 0]
                else:
                    continue

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

                self.ground.blit(image, pos * WorldGeneration.TILE_SIZE)
                pos = next_pos
                direction = next_direction
            destination_nodes = nodes[edge[0][1]]
            if destination_nodes[1][1] == "poi":
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
                    case (0, 0):
                        # TODO
                        # might cause an error
                        image = pygame.image.load("Sprites/PathTiles/straight.png")
                    case _:
                        raise ValueError("poi direction not found")

            if not image:
                continue

            self.ground.blit(image, pos * WorldGeneration.TILE_SIZE)

    @staticmethod
    def generate_perlin_noise(width, height, scale=100.0, octaves=6, seed=None, is_debug=False):
        noise_gen = PerlinNoise(octaves=octaves, seed=seed)

        world = np.zeros((height, width))

        for i in range(height):
            for j in range(width):
                world[i][j] = noise_gen([i / scale, j / scale])

        # Display the Perlin noise sample
        if is_debug:
            plt.imshow(world, cmap='gray', interpolation='bilinear')
            plt.colorbar()
            plt.show()

        return world

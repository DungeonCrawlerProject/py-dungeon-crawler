import pygame
from typing import Optional
from Scripts.GameObject.game_object import GameObject
from Scripts.CollisionBox.collision_handler import CollisionHandler


class CollisionBox(GameObject):
    def __init__(
        self,
        position: pygame.Vector2,
        dimensions: pygame.Vector2,
        collision_handler: CollisionHandler,
        tag: Optional[str] = None,
    ) -> None:
        super().__init__(position=position, sprite=None, tag=tag)
        self.dimensions = dimensions
        self.collision_handler = collision_handler
        self.parent = None

    def add_parent(self, parent: GameObject):
        self.parent = parent

    def update(self):
        if self.parent is not None:
            self.position = self.parent.position

    def check_collision(self):
        collisions = []
        for collider in self.collision_handler.active_coliders:
            if collider == self:
                continue
            collider_a_in = self.position[0] < collider.position[0] < self.position[0] + self.dimensions[0]
            collider_b_in = self.position[0] < collider.position[0] + collider.dimensions[0] < self.position[0] + self.dimensions[0]
            collider_c_in = self.position[1] < collider.position[1] < self.position[1] + self.dimensions[1]
            collider_d_in = self.position[1] < collider.position[1] + collider.dimensions[1] < self.position[1] + self.dimensions[1]
            if collider_a_in or collider_b_in:
                if collider_c_in or collider_d_in:
                    collisions.append(collider)

            collider_w_in = collider.position[0] < self.position[0] < collider.position[0] + collider.dimensions[0]
            collider_x_in = collider.position[0] < self.position[0] + self.dimensions[0] < collider.position[0] + collider.dimensions[0]
            collider_y_in = collider.position[1] < self.position[1] < collider.position[1] + collider.dimensions[1]
            collider_z_in = collider.position[1] < self.position[1] + self.dimensions[1] < collider.position[1] + collider.dimensions[1]
            if collider_w_in or collider_x_in:
                if collider_y_in or collider_z_in:
                    collisions.append(collider)

        return collisions
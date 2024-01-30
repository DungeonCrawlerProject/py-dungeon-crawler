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
        self.rect = pygame.Rect(position, dimensions)
        self.collision_handler = collision_handler
        self.parent = None

    def add_parent(self, parent: GameObject):
        self.parent = parent

    def update(self):
        if self.parent is not None:
            self.position = self.parent.position
            #TODO
            #this feels bad
            self.rect.x = self.parent.position[0]
            self.rect.y = self.parent.position[1]

    def check_collision(self):
        collisions = self.rect.collideobjectsall(self.collision_handler.active_colliders)
        return collisions
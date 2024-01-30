import pygame
from typing import Optional
from Scripts.GameObject.game_object import GameObject
from Scripts.CollisionBox.collision_handler import CollisionHandler


class CollisionBox(pygame.Rect):
    def __init__(
        self,
        position: pygame.Vector2,
        dimensions: pygame.Vector2,
        collision_handler: CollisionHandler,
        tag: Optional[str] = None,
    ) -> None:
        super().__init__(position, dimensions)
        self.collision_handler = collision_handler
        collision_handler.active_colliders[tag].append(self)

    def check_collision(self):
        collisions = self.rect.collideobjectsall(self.collision_handler.active_colliders)
        return collisions
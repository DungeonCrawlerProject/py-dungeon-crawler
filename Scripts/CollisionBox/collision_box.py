import pygame
from typing import Optional
from Scripts.CollisionBox.collision_handler import CollisionHandler


class CollisionBox(pygame.Rect):
    def __init__(
        self,
        parent,
        position: pygame.Vector2,
        dimensions: pygame.Vector2,
        collision_handler: CollisionHandler,
        tag: Optional[str] = None,
    ) -> None:
        """the collision box is associated with objects that are collidable and
          is used to check what other objects its associated object is colliding with

        Args:
            parent (object): The parent object of the collision box.
            position (pygame.Vector2): the position of the collision box
            dimensions (pygame.Vector2): the width and height of the collision box
            collision_handler (CollisionHandler): the collision handler associated with this collider
            tag (Optional[str], optional): used to differentiate collision boxes by types. Defaults to None.
        """
        super().__init__(position, dimensions)
        self.collision_handler = collision_handler
        collision_handler.active_colliders[tag].append(parent)

    def check_collision(self, tag: Optional[str] = None) -> list:
        """Checks for all other collisions boxes that are within this collision box,
        if tag is passed in it will only check for objects with that tag.

        Args:
            tag (Optional, str): used to specify objects to check. Defaults to None.

        Returns:
            list: a list of objects that collide with this box.
        """
        if tag == None:
            collisions = []
            for key in self.collision_handler:
                collisions.append(self.collideobjectsall(self.collision_handler.active_colliders[key], key=lambda x: x.collider))
        else:
            collisions = self.collideobjectsall(self.collision_handler.active_colliders[tag], key=lambda x: x.collider)
        return collisions
    
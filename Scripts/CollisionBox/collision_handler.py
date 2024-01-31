from collections import defaultdict
from typing import Optional

class CollisionHandler:
    def __init__(self) -> None:
        """stores a dictinary of all active collision boxes in the game.

        Params:
        active_colliders
        """
        self.active_colliders = defaultdict(list)

    def add_collider(self, collider, tag: Optional[str] = "generic"):
        self.active_colliders[tag].append(collider)

    def remove_collider(self, collider):
        self.active_colliders.remove(collider)

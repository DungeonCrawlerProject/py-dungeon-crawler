from collections import defaultdict
from typing import Optional

class CollisionHandler:
    def __init__(self) -> None:
        self.active_colliders = defaultdict(list)

    def add_collider(self, collider, tag: Optional[str] = "generic"):
        self.active_colliders[tag].append(collider)

    def remove_collider(self, collider):
        self.active_colliders.remove(collider)

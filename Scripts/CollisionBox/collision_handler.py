

class CollisionHandler:
    def __init__(self) -> None:
        self.active_colliders = []

    def update(self):
        for collider in self.active_colliders:
            collider.update()
            print(collider.position)

    def add_collider(self, collider):
        self.active_colliders.append(collider)

    def remove_collider(self, collider):
        self.active_colliders.remove(collider)

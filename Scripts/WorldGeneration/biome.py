from typing import List

from pydantic import BaseModel


class Biome(BaseModel):
    name: str
    tile_set: str
    points_of_interest: List[str]
    environment_objects: List[str]

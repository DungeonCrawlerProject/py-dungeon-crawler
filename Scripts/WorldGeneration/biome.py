import json
from typing import List

from pydantic import BaseModel


class Biome(BaseModel):
    name: str
    tile_set: str
    points_of_interest: List[str]
    environment_objects: List[str]

    @classmethod
    def from_json(cls, path):

        with open(path, "r") as file:
            biome_data = json.load(file)
        inst = cls(**biome_data)

        return inst


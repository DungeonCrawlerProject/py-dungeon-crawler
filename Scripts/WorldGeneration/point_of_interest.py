import json
from typing import List

from pydantic import BaseModel


class PointOfInterest(BaseModel):
    name: str
    sprite_sheet: str
    size: List[int]

    @classmethod
    def from_json(cls, path):
        with open(path, "r") as file:
            biome_data = json.load(file)
        inst = cls(**biome_data)

        return inst
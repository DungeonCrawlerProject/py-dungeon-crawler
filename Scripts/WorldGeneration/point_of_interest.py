from typing import List

from pydantic import BaseModel


class PointOfInterest(BaseModel):
    name: str
    sprite_sheet: str
    size: List[int]

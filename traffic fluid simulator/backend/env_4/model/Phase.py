from dataclasses import dataclass
from typing import List, Tuple
import attr


@attr.s(auto_attribs=True, frozen=True)
class Phase:
    index: int
    moves: List[Tuple[int, int]]

from dataclasses import dataclass
from typing import List


@dataclass
class Phase:
    moves: List[tuple]
    number: int

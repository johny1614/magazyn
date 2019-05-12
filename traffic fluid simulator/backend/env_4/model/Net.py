from typing import List

import attr


@attr.s(auto_attribs=True,frozen=True)
class Net:
    lights: List[List[float]]
    densities: List[float]


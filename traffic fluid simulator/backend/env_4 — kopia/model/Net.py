from typing import List

import attr


@attr.s(auto_attribs=True)
class Net: # to jest dawane na front
    lights: List[List[float]] # 36 x 36 liczb
    densities: List[float] # 36 liczb
    rewards: List[float]


from typing import List

import attr

@attr.s(auto_attribs=True)
class Times:
    old_time: int
    new_time: int


@attr.s(auto_attribs=True)
class Net: # to jest dawane na front
    times: Times
    rewards: List[float] # 3 liczby
    actions: List[float] # 3 liczby
    densities: List[float] # 36 liczb
    lights: List[List[float]] = attr.ib(factory=list) # 36 x 36 liczb


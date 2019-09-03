from typing import List
import attr


@attr.s(auto_attribs=True)
class Times:
    old_time: int
    new_time: int


@attr.s(auto_attribs=True)
class Net:  # to jest przekazywane dalej na front
    times: Times
    rewards: List[float]
    actions: List[int]
    densities: List[float]
    lights: List[List[float]] = attr.ib(factory=list)  # 36 x 36 liczb

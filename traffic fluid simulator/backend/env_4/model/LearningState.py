from typing import Tuple

import attr


@attr.s(auto_attribs=True, frozen=True)
class LearningState:
    pre_cross_densities: Tuple[int]
    global_aggregated_densities: Tuple[int]
    phase_index: int
    phase_duration: int

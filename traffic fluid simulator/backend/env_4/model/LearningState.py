from dataclasses import dataclass
from typing import Tuple
from services.hashable_decorator import hashable


@hashable()
@dataclass
class LearningState:
    pre_cross_densities: Tuple[int]
    global_aggregated_densities: Tuple[int]
    phase_no: int
    phase_duration: int
    hash_keys = ['pre_cross_densities', 'global_aggregated_densities', 'phase_no', 'phase_duration']

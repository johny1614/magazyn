from dataclasses import dataclass
from typing import List

from services.hashable_decorator import hashable


@hashable()
@dataclass
class LearningState:
    pre_cross_densities: tuple
    global_aggregated_densities: tuple
    phase_no: int
    phase_duration: int
    hash_keys=['pre_cross_densities','global_aggregated_densities','phase_no','phase_duration']

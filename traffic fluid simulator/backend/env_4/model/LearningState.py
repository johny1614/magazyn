from dataclasses import dataclass
from typing import List


@dataclass
class LearningState:
    pre_cross_densities: List[int]
    global_aggregated_densities: List
    phase_no: int
    phase_duration: int

    def __eq__(self, other):
        all_properties = [prop for prop in dir(self) if not prop.startswith('__')]
        for prop in all_properties:
            if getattr(self, prop) != getattr(other, prop):
                return False
        return True

    def __hash__(self):
        all_properties = [prop for prop in dir(self) if not prop.startswith('__')]
        values = tuple([getattr(self, prop) for prop in all_properties])
        return hash(values)

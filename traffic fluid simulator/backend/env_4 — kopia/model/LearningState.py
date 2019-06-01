from typing import Tuple
import attr
import numpy as np


@attr.s(auto_attribs=True, cmp=False)
class LearningState:
    pre_cross_densities: Tuple[int]
    global_aggregated_densities: Tuple[int]
    phase_index: int
    phase_duration: int

    def __attrs_post_init__(self):
        self.cluster_index: int = 0

    def __hash__(self):
        all_properties = ['pre_cross_densities', 'global_aggregated_densities', 'phase_index', 'phase_duration']
        values = tuple([getattr(self, prop) for prop in all_properties])
        return hash(values)

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
    def to_nd_array(self):
        return np.array([self.to_array()])
    def to_array(self):
        array = []
        for den in self.pre_cross_densities:
            array.append(den)
        for den in self.global_aggregated_densities:
            array.append(den)
        array.append(self.phase_index)
        array.append(self.phase_duration)
        return array
    @staticmethod
    def from_array(arr):
        return LearningState(pre_cross_densities=tuple(arr[0:3]),global_aggregated_densities=tuple(arr[3:15]),phase_index=arr[15],phase_duration=arr[16])




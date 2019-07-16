from typing import Tuple, List
import attr
import numpy as np


@attr.s(auto_attribs=True, cmp=False)
class LearningState:
    pre_cross_densities: Tuple[int]
    global_aggregated_densities: Tuple[int]
    actual_phase: int
    starting_actual_phase: int  # do learningu jest potrzebny stan ktory jest de facto w t-1 i jest na poczatku t i wlasnie w t jest zmieniany
    phase_duration: int
    global_densities: List[int]
    densities: List[int]

    def __attrs_post_init__(self):
        self.cluster_index: int = 0

    def __hash__(self):
        all_properties = ['pre_cross_densities', 'global_aggregated_densities', 'actual_phase', 'phase_duration']
        values = tuple([getattr(self, prop) for prop in all_properties])
        return hash(values)

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def to_learn_array(self):
        return np.array([[self.densities[0]] + [self.densities[1]] + [self.starting_actual_phase]])

    def possible_actions(self, orange_phase_duration):
        wait_action = ['orange']
        light_Actions = [0, 1]
        if self.phase_duration >= orange_phase_duration:
            return light_Actions
        return wait_action

    @staticmethod
    def from_array(arr):
        return LearningState(pre_cross_densities=tuple(arr[0:3]), global_aggregated_densities=tuple(arr[3:15]),
                             phase_index=arr[15], phase_duration=arr[16])

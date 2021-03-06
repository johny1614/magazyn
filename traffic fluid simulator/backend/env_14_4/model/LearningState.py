from typing import Tuple, List
import attr
import numpy as np


@attr.s(auto_attribs=True, cmp=False)
class LearningState:
    actual_phase: int
    starting_actual_phase: int  # do learningu jest potrzebny stan ktory jest de facto w t-1 i jest na poczatku t i wlasnie w t jest zmieniany
    phase_duration: int
    global_densities: List[int]
    densities: List[int]
    orange_phase_duration: int

    def __attrs_post_init__(self):
        self.cluster_index: int = 0

    def __hash__(self):
        all_properties = ['actual_phase', 'phase_duration']
        values = tuple([getattr(self, prop) for prop in all_properties])
        return hash(values)

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def to_learn_array(self):
        phase_0 = self.starting_actual_phase == 0
        phase_1 = self.starting_actual_phase == 1
        phase_orange = self.starting_actual_phase == 'orange'
        left_orange_time = max(self.orange_phase_duration-self.phase_duration,0)
        return np.array([[self.densities[0]] + [self.densities[1]]+[self.densities[2]]+[self.densities[3]]+[phase_0]+[phase_1]+[phase_orange]+[left_orange_time]])

    def possible_actions(self, orange_phase_duration):
        wait_action = ['orange']
        light_Actions = [0, 1]
        if self.phase_duration >= orange_phase_duration:
            return light_Actions
        return wait_action

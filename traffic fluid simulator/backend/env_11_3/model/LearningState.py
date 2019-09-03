from typing import Tuple, List
import attr
import numpy as np

yellow = 'yellow'


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

    def to_learn_array(self):
        return np.array([[self.densities[0]] + [self.densities[1]]])

    def possible_actions(self, yellow_phase_duration):
        wait_action = [yellow]
        light_Actions = [0, 1]
        if self.phase_duration >= yellow_phase_duration:
            return light_Actions
        return wait_action

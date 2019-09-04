from typing import Tuple, List
import attr
import numpy as np

from model.Action import yellow


@attr.s(auto_attribs=True, cmp=False)
class LearningState:
    actual_phase: int
    starting_actual_phase: int  # do learningu jest potrzebny stan ktory jest de facto w t-1 i jest na poczatku t i wlasnie w t jest zmieniany
    phase_duration: int
    global_densities: List[int]
    densities: List[int]
    yellow_phase_duration: int

    def __attrs_post_init__(self):
        self.cluster_index: int = 0


    def to_learn_array(self, agent):
        phase = self.starting_actual_phase
        if phase == yellow and self.actual_phase != yellow:
            phase = self.actual_phase
        is_0_phase = phase == 0
        is_1_phase = phase == 1
        is_2_phase = phase == 2
        # gdy zaczynamy z yellow to de facto mamy juz nowa faze do decyzji - ale decydujemy zawsze podtrzymanie tego swiatla na chociaz 1 ture
        return np.array([[self.densities[sec] for sec in agent.local_phase_sections] + [
            is_0_phase] + [is_1_phase] + [is_2_phase]])

    def possible_actions(self, yellow_phase_duration):
        wait_action = [yellow]
        light_Actions = [0, 1, 2]
        if self.phase_duration >= yellow_phase_duration:
            return light_Actions
        return wait_action

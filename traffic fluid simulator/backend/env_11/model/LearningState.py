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

    def den_group(self, den):
        den_group = None
        if den == 0:
            den_group = 0
        elif 0 < den <= 5:
            den_group = 1
        elif 5 < den <= 10:
            den_group = 2
        elif 10 < den <= 20:
            den_group = 3
        elif 20 < den <= 40:
            den_group = 4
        elif 40 < den <= 50:
            den_group = 5
        elif 50 < den <= 90:
            den_group = 6
        elif 90 < den <= 200:
            den_group = 7
        else:
            den_group = 8
        return den_group

    def to_learn_nd_array_full(self):
        return np.array([self.global_densities + [self.actual_phase]])

    def to_learn_nd_array(self):
        return np.array([[self.pre_cross_densities[0], self.pre_cross_densities[1], self.pre_cross_densities[2],
                          self.actual_phase]])

    def to_learn_array_1_density(self):
        return np.array([[self.densities[0]] + [self.starting_actual_phase]])

    def to_learn_tuple_used(self):
        den0 = round(self.densities[0], 0)
        den1 = round(self.densities[1], 0)
        return (den0, den1 , self.actual_phase)

    def to_learn_nd_array_densities_group(self):
        den_group0 = self.den_group(self.pre_cross_densities[0])
        den_group1 = self.den_group(self.pre_cross_densities[1])
        den_group2 = self.den_group(self.pre_cross_densities[2])
        actual_phase = self.actual_phase
        if den_group0 is None or den_group1 is None or den_group2 is None:
            pass
        return np.array([[den_group0, den_group1, den_group2, actual_phase]])

    def to_nd_array(self):
        return np.array([self.to_array()])

    def to_array(self):
        array = []
        for den in self.pre_cross_densities:
            array.append(den)
        for den in self.global_aggregated_densities:
            array.append(den)
        array.append(self.actual_phase)
        array.append(self.phase_duration)
        return array

    def possible_actions(self, orange_phase_duration):
        wait_action = [0]
        light_Actions = [1, 2, 3]
        if self.phase_duration >= orange_phase_duration:
            return light_Actions
        return wait_action

    @staticmethod
    def from_array(arr):
        return LearningState(pre_cross_densities=tuple(arr[0:3]), global_aggregated_densities=tuple(arr[3:15]),
                             phase_index=arr[15], phase_duration=arr[16])

from dataclasses import dataclass
from typing import Any

from env_data import sections_of_roads
from model.LearningState import LearningState
from services.densityGroups import getGroup
import numpy as np


@dataclass
class Agent:
    all_phases: Any
    actual_phase: Any
    min_phase_duration: int
    index: int
    local_phase_sections: Any
    phase_duration: Any
    curve_densities: Any
    orange_phase_duration: int = 1

    def __init__(self):
        self.pending_action_no = 0
        self.local_state = None
        self.actual_phase_no = None
        self.t = 0

    def getLocalActionSpace(self):
        waitActions = ['wait']
        light_Actions = [1, 2, 3]
        if self.phase_duration >= self.min_phase_duration:
            return light_Actions
        return waitActions

    def modify_A(self, A):
        if self.actual_phase == [[]]:
            return A
        for manewr in self.actual_phase:
            if manewr == []:
                continue
            A[manewr] = self.curve_densities[manewr]
            fromSection = manewr[1]
            A[fromSection][fromSection] -= A[manewr]
        return A

    def pass_action(self, action):
        if action == 'wait':
            self.phase_duration += 1
            if self.actual_phase == self.all_phases[0] and self.phase_duration == self.orange_phase_duration:
                self.actual_phase = self.all_phases[self.pending_action_no]
                self.actual_phase_no = self.pending_action_no
        # else:
        #     if self.all_phases[action] == self.actual_phase:
        #         self.phase_duration += 1
        #     else:  # nowa akcja!
        #         self.phase_duration = 0
        #         print('zerowanie!')
        #         if self.phase_duration == self.orange_phase_duration:
        #             self.actual_phase = self.all_phases[action]
        #             self.actual_phase_no = action
        #         else:
        #             self.actual_phase = self.all_phases[0]  # orange
        #             self.actual_phase_no = 0
        #             self.pending_action_no = action
        self.t += 1

    def assignLocalState(self, densities):
        pre_cross_densities = ()
        for sec in self.local_phase_sections:
            pre_cross_densities = pre_cross_densities + (getGroup(densities[sec]),)
        global_aggregated_densities = ()
        for road in sections_of_roads:
            global_aggregated_densities = global_aggregated_densities + (np.mean([getGroup(den) for den in road]),)
        self.local_state = LearningState(pre_cross_densities, global_aggregated_densities, self.actual_phase_no,
                                         self.phase_duration)

from dataclasses import dataclass
from typing import Any, List, Dict, Tuple

import attr

from env_data import sections_of_roads
from model.LearningState import LearningState
from model.Phase import Phase
from services.densityGroups import getGroup
import numpy as np


@attr.s(auto_attribs=True)
class Agent:
    index: int
    all_phases: List[Phase]
    local_phase_sections: List[int]
    curve_densities: Dict[Tuple[int, int], int]
    min_phase_duration: int = 0
    local_state: LearningState = None


    def __attrs_post_init__(self):
        self.actual_phase: Phase = self.all_phases[0]
        self.orange_phase_duration: int = 1
        # self.min_phase_duration: int = 3
        self.phase_duration: int = 0

    # def __init__(self):
    #     self.pending_action_no = 0
    #     self.local_state = None
    #     self.actual_phase_no = None
    #     self.t = 0

    def get_local_action_space(self):
        waitActions = ('wait')
        light_Actions = (1, 2, 3)
        if self.phase_duration >= self.min_phase_duration:
            return light_Actions
        return waitActions

    def modify_A(self, A):
        if self.actual_phase.index == 0:
            return A
        for move in self.actual_phase.moves:
            if move == []:
                continue
            A[move] = self.curve_densities[move]
            fromSection = move[1]
            A[fromSection][fromSection] -= A[move]
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

    def assignLocalState(self, densities):
        pre_cross_densities = ()
        for sec in self.local_phase_sections:
            pre_cross_densities = pre_cross_densities + (getGroup(densities[sec]),)
        global_aggregated_densities = ()
        for road in sections_of_roads:
            global_aggregated_densities = global_aggregated_densities + (np.mean([getGroup(den) for den in road]),)
        self.local_state = LearningState(pre_cross_densities=pre_cross_densities,
                                         global_aggregated_densities=global_aggregated_densities,
                                         phase_index=self.actual_phase.index,
                                         phase_duration=self.phase_duration)

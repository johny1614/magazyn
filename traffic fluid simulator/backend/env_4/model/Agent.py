from typing import List, Dict, Tuple

import attr
import numpy as np

from env_data import sections_of_roads
from model.Action import Action
from model.LearningState import LearningState
from model.Phase import Phase
from services.densityGroups import getGroup


@attr.s(auto_attribs=True)
class Agent:
    index: int
    all_phases: List[Phase]
    local_phase_sections: List[int]
    curve_densities: Dict[Tuple[int, int], int]
    phase_duration: int = 10
    orange_phase_duration: int = 1
    local_state: LearningState = None
    pending_phase: Phase = None
    rewards: List[float] = []

    def __attrs_post_init__(self):
        self.actual_phase: Phase = self.all_phases[0]

    @property
    def local_action_space(self) -> Tuple[Action]:
        wait_action = (Action(0, self.index, self.all_phases[0]),)
        light_Actions = ()
        for phase in self.all_phases[1:]:
            light_Actions += (Action(phase.index, self.index, self.all_phases[phase.index]),)
        if self.phase_duration >= self.orange_phase_duration:
            return light_Actions
        return wait_action

    def modify_A(self, A):
        print('modify', self.actual_phase.index)
        if self.actual_phase.index == 0:
            return A
        for move in self.actual_phase.moves:
            if move == []:
                continue
            # print('move', move)
            A[move] = self.curve_densities[move]
            fromSection = move[1]
            A[fromSection][fromSection] -= A[move]
        return A

    def pass_action(self, action: Action):
        if (action not in self.local_action_space):
            print('action not in local action space!', 2 / 0)
        if action.index == 0:  # wait
            self.phase_duration += 1
            if self.actual_phase.index == 0 and self.phase_duration == self.orange_phase_duration:
                self.actual_phase = self.pending_phase
            else:
                print('B')
                pass
        elif action.index != 0:
            if (action.index == self.actual_phase.index):
                print('C')
                self.phase_duration += 1
            else:
                self.pending_phase = action.decided_phase
                self.phase_duration = 0
                self.actual_phase = self.all_phases[0]
                if (self.phase_duration >= self.orange_phase_duration):
                    self.actual_phase = self.pending_phase
                    print('E')
                else:
                    print('D')

    def assign_local_state(self, densities):
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

    def assign_reward(self, previous_x, actual_x, global_reward):
        # TODO dodac lokalny reward
        self.rewards.append(global_reward)

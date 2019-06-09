from typing import Any, List, Dict, Tuple
import attr
import random
from env_data import sections_of_roads
from model.LearningState import LearningState
from model.Phase import PhaseInt
import numpy as np

from services.globals import Globals

ActionInt = int


@attr.s(auto_attribs=True)
class Agent:
    index: int
    moves: List[Tuple[int, int]]
    local_phase_sections: List[int]
    curve_densities: Dict[Tuple[int, int], int]
    local_state: LearningState = None
    phase_duration: int = 0
    orange_phase_duration: int = 0
    pending_phase: PhaseInt = None
    rewards: List[float] = []
    actual_phase = 0
    action = 0

    @property
    def local_action_space(self) -> Tuple[ActionInt]:
        wait_action = [0]
        light_Actions = [1, 2, 3]
        if self.phase_duration >= self.orange_phase_duration:
            return light_Actions
        return wait_action

    def modify_A(self, A):
        actual_moves = self.moves[self.actual_phase]
        # print(f'agent:{self.index} phase {self.actual_phase} i jego moves: {actual_moves}')
        for move in actual_moves:
            A[move] = self.curve_densities[move]
            fromSection = move[1]
            A[fromSection][fromSection] -= A[move]

        return A

    def pass_action(self,action: ActionInt):
        self.action=action
        if action not in self.local_action_space:
            print(f'uwagaAAAAAAAAAAAAAAAAAAA akcja {action} nie jest w local_action_space')
        if action == 0:
            if self.actual_phase==0:
                self.phase_duration+=1
            else:
                self.actual_phase=0
                self.phase_duration=0
            if self.phase_duration>=self.orange_phase_duration:
                self.actual_phase=self.pending_phase
                self.phase_duration=0
        if action != 0:
            if action==self.actual_phase:
                self.phase_duration+=1
            else:
                self.phase_duration=0
                self.pending_phase=action
            if self.phase_duration>=self.orange_phase_duration:
                self.actual_phase=self.pending_phase
            else:
                self.actual_phase=0

    def assign_local_state(self, densities):
        pre_cross_densities = ()
        for sec in self.local_phase_sections:
            pre_cross_densities = pre_cross_densities + (densities[sec],)
        global_aggregated_densities = ()
        for road in sections_of_roads:
            global_aggregated_densities = global_aggregated_densities + (
                round(np.sum([densities[section] for section in road])),)
        local_state = LearningState(pre_cross_densities=pre_cross_densities,
                                    global_aggregated_densities=global_aggregated_densities,
                                    phase_index=self.actual_phase,
                                    phase_duration=self.phase_duration)
        self.local_state = local_state

    def assign_reward(self, previous_x, actual_x, global_reward):
        # TODO dodac lokalny reward
        self.rewards.append(global_reward)

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
    phase_duration: int = 2  # na starcie mamy mozliwosc przelaczania - taki bonus
    orange_phase_duration: int = 2
    pending_phase: PhaseInt = 1
    rewards: List[float] = []
    actual_phase = 1
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

    def pass_action(self, action: ActionInt):
        # if action not in self.local_action_space:
        #     print(
        #         f'uwagaAAAAAAAAAAAAAAAAAAA akcja {action} nie jest w local_action_space ktory jest rowny {self.local_action_space}')
        #     if self.local_action_space == [0]:
        #         action = 0
        #         print('akcja zmieniona na 0')
        self.action = action
        # if 60 <= Globals().time <= 63 and self.index == 0:
        # print(f'Na poczatku chwili {Globals().time} jest faza {self.actual_phase} akcja to:{action} phase_duration:{self.phase_duration} pending_phase:{self.pending_phase}')
        if action == 0:
            if self.actual_phase == 0:
                self.phase_duration += 1
            else:
                self.actual_phase = 0
                self.phase_duration = 0
                # print('a')
            if self.phase_duration >= self.orange_phase_duration:
                self.actual_phase = self.pending_phase
                # print('b')
                # self.phase_duration = 0
        if action != 0:
            if action == self.actual_phase:
                self.phase_duration += 1
            else:
                if action == self.pending_phase:
                    self.phase_duration += 1
                else:
                    self.phase_duration = 0
                    self.pending_phase = action
                    self.actual_phase = 0
                if self.phase_duration >= self.orange_phase_duration:
                    self.actual_phase = self.pending_phase
        self.local_state.actual_phase=self.actual_phase
        # if 60 <= Globals().time <= 63 and self.index == 0:
        #     print(f'Na koniec   chwili {Globals().time} jest faza {self.actual_phase} akcja to:{action} phase_duration:{self.phase_duration} pending_phase:{self.pending_phase}')

    def assign_local_state(self, densities):
        pre_cross_densities = ()
        for sec in self.local_phase_sections:
            pre_cross_densities = pre_cross_densities + (densities[sec],)
        global_aggregated_densities = ()
        global_densities = []
        for road in sections_of_roads:
            global_aggregated_densities = global_aggregated_densities + (
                round(np.sum([densities[section] for section in road])),)
            for sec in road:
                global_densities.append(densities[sec])
        local_state = LearningState(pre_cross_densities=pre_cross_densities,
                                    global_aggregated_densities=global_aggregated_densities,
                                    global_densities=global_densities,
                                    actual_phase=self.actual_phase,
                                    phase_duration=self.phase_duration)
        self.local_state = local_state

from typing import List, Dict, Tuple

import attr
import numpy as np

from env_settings import sections_of_roads
from model.Action import ActionInt
from model.LearningState import LearningState
from model.Phase import PhaseInt
from services.globals import Globals


@attr.s(auto_attribs=True)
class Agent:
    index: int
    moves: List[Tuple[int, int]]
    local_phase_sections: List[int]
    curve_densities: Dict[Tuple[int, int], int]
    local_state: LearningState = None
    phase_duration: int = 2  # na starcie mamy mozliwosc przelaczania - taki bonus
    orange_phase_duration: int = 2
    pending_phase: PhaseInt = 0
    rewards: List[float] = []
    actual_phase = 0
    starting_actual_phase = 0
    action = None

    @property
    def local_action_space(self) -> Tuple[ActionInt]:
        wait_action = ['orange']
        light_Actions = [0, 1, 2, 3]
        if self.phase_duration >= self.orange_phase_duration:
            return light_Actions
        return wait_action

    def modify_A(self, A):
        actual_moves = () if self.actual_phase == 'orange' else self.moves[self.actual_phase]
        for move in actual_moves:
            A[move] = self.curve_densities[move]
            fromSection = move[1]
            A[fromSection][fromSection] -= A[move]
        return A

    def pass_action(self, action: ActionInt):
        if action not in self.local_action_space:
            if self.local_action_space == ['orange']:
                action = 'orange'
            # print(
            #     f'uwagaAAAAAAAAAAAAAAAAAAA akcja {action} nie jest w local_action_space ktory jest rowny {self.local_action_space}, w chwili {Globals().time}, aktualny phase_duration: {self.phase_duration}, aktualna faza: {self.actual_phase}')
        self.action = action
        orange = 'orange'
        if action == orange:
            if self.actual_phase == orange:
                self.phase_duration += 1
            else:
                self.actual_phase = orange
                self.phase_duration = 0
            if self.phase_duration >= self.orange_phase_duration:
                self.actual_phase = self.pending_phase
                self.starting_actual_phase = self.actual_phase  # jak sie zrobi faza z orange na np.1 to juz mamy starting_actual_phase=1 do uczenia a nie orange
        if action != orange:
            if action == self.actual_phase:
                self.phase_duration += 1
            else:
                if action == self.pending_phase:
                    self.phase_duration += 1
                else:
                    self.phase_duration = 0
                    self.pending_phase = action
                    self.actual_phase = orange
                if self.phase_duration >= self.orange_phase_duration:
                    self.actual_phase = self.pending_phase
        self.local_state.actual_phase = self.actual_phase

    def assign_local_state(self, densities):
        global_densities = []
        for road in sections_of_roads:
            for sec in road:
                global_densities.append(densities[sec])
        local_state = LearningState(global_densities=global_densities,
                                    actual_phase=self.actual_phase,
                                    phase_duration=self.phase_duration,
                                    densities=densities,
                                    starting_actual_phase=self.actual_phase,
                                    orange_phase_duration=self.orange_phase_duration)
        self.local_state = local_state

from typing import List, Dict, Tuple
import attr
from env_settings import sections_of_roads
from model.Action import ActionInt
from model.LearningState import LearningState
from model.Phase import PhaseInt

yellow = 'yellow'


@attr.s(auto_attribs=True)
class Agent:
    index: int
    moves: List[Tuple[int, int]]
    local_phase_sections: List[int]
    curve_densities: Dict[Tuple[int, int], int]
    local_state: LearningState = None
    phase_duration: int = 0
    yellow_phase_duration: int = 0
    pending_phase: PhaseInt = 1
    rewards: List[float] = []
    actual_phase = 1
    starting_actual_phase = 1
    action = None

    @property
    def local_action_space(self) -> List[ActionInt]:
        wait_action = [yellow]
        light_Actions = [0, 1]
        if self.phase_duration >= self.yellow_phase_duration:
            return light_Actions
        return wait_action

    def modify_A(self, A):
        actual_moves = () if self.actual_phase == yellow else self.moves[self.actual_phase]
        for move in actual_moves:
            if move[0] == 404:
                continue
            A[move] = self.curve_densities[move]
            fromSection = move[1]
            A[fromSection][fromSection] -= A[move]
        return A

    def pass_action(self, action: ActionInt):
        if action not in self.local_action_space:
            if self.local_action_space == [yellow]:
                action = yellow
        self.action = action
        if action == yellow:
            if self.actual_phase == yellow:
                self.phase_duration += 1
            else:
                self.actual_phase = yellow
                self.phase_duration = 0
            if self.phase_duration >= self.yellow_phase_duration:
                self.actual_phase = self.pending_phase
        if action != yellow:
            if action == self.actual_phase:
                self.phase_duration += 1
            else:
                if action == self.pending_phase:
                    self.phase_duration += 1
                else:
                    self.phase_duration = 0
                    self.pending_phase = action
                    self.actual_phase = yellow
                if self.phase_duration >= self.yellow_phase_duration:
                    self.actual_phase = self.pending_phase
        self.local_state.actual_phase = self.actual_phase

    def assign_local_state(self, densities):
        pre_cross_densities = ()
        for sec in self.local_phase_sections:
            pre_cross_densities = pre_cross_densities + (densities[sec],)
        global_aggregated_densities = ()
        global_densities = []
        for road in sections_of_roads:
            for sec in road:
                global_densities.append(densities[sec])
        local_state = LearningState(pre_cross_densities=pre_cross_densities,
                                    global_aggregated_densities=global_aggregated_densities,
                                    global_densities=global_densities,
                                    actual_phase=self.actual_phase,
                                    phase_duration=self.phase_duration,
                                    densities=densities,
                                    starting_actual_phase=self.actual_phase)
        self.local_state = local_state

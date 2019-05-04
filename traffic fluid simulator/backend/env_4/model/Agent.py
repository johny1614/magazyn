import random

from env_data import sections_of_roads
from services.densityGroups import getGroup
import numpy as np


class Agent:
    def __init__(self, dic, min_phase_duration, index, orange_phase_duration=1):
        self.index = index
        self.min_phase_duration = min_phase_duration
        self.all_phases = dic['all_phases']
        self.actual_phase_no=None
        self.actual_phase = dic['actual_phase']  # sometimes the pending one
        self.local_state = None
        self.local_phase_sections = dic['local_phase_sections']
        self.pending_action_no = 1
        self.phase_duration = dic['actual_phase_duration']
        self.curve_densities = dic['curve_densities']
        self.orange_phase_duration = orange_phase_duration
        self.t = 0

    def getLocalActionSpace(self):
        waitActions = ['wait']
        light_Actions = [1, 2, 3]
        if (self.phase_duration >= self.min_phase_duration):
            return light_Actions
        return waitActions

    def getRandomAction(self):
        return random.choice(self.getLocalActionSpace())

    def modify_A(self, A):
        if (self.actual_phase == [[]]):
            return A
        for manewr in self.actual_phase:
            if (manewr == []):
                continue
            A[manewr] = self.curve_densities[manewr]
            fromSection = manewr[1]
            A[fromSection][fromSection] -= A[manewr]
        return A

    def pass_action(self, action):
        if (action == 'wait'):
            self.phase_duration += 1
            if (self.actual_phase == self.all_phases[0] and self.phase_duration == self.orange_phase_duration):
                self.actual_phase = self.all_phases[self.pending_action_no]
                self.actual_phase_no=self.pending_action_no
        else:
            if (self.all_phases[action] == self.actual_phase):
                self.phase_duration += 1
            else:  # nowa akcja!
                self.phase_duration = 0
                if (self.phase_duration == self.orange_phase_duration):
                    self.actual_phase = self.all_phases[action]
                    self.actual_phase_no = action
                else:
                    self.actual_phase = self.all_phases[0]  # orange
                    self.actual_phase_no = 0
                    self.pending_action_no = action
        self.t += 1

    def assignLocalState(self, densities):
        pre_cross_densities = []
        for sec in self.local_phase_sections:
            pre_cross_densities.append(getGroup(densities[sec]))
        global_aggregated_densities = []
        for road in sections_of_roads:
            global_aggregated_densities.append(np.mean([getGroup(den) for den in road]))
        self.local_state = LocalState(pre_cross_densities,global_aggregated_densities,self.actual_phase_no,self.phase_duration)


class LocalState:
    def __init__(self, pre_cross_densities, global_aggregated_densities,phase_no,phase_duration):
        self.pre_cross_densities = pre_cross_densities
        self.global_aggregated_densities = global_aggregated_densities
        self.phase_no = phase_no
        self.phase_duration = phase_duration

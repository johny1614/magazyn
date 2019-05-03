import random


class Agent:
    def __init__(self, dic, min_phase_duration, index, orange_phase_duration=1):
        self.index = index
        self.min_phase_duration = min_phase_duration
        self.all_phases = dic['all_phases']
        self.actual_phase = dic['actual_phase']  # sometimes the pending one
        self.pending_action_number = None
        # self.stay_manewr = dic['stay_manewr'] # odpowiada za te kumulujace sie przed czerwonym swiatlem
        self.real_phase = dic['actual_phase']  # the one changing A matrix
        self.phase_duration = dic['actual_phase_duration']
        self.curve_densities = dic['curve_densities']
        self.possible_actions = self.getLocalActionSpace()
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
        if (self.real_phase == 'wait'):
            return A
        for manewr in self.real_phase:
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
                self.actual_phase = self.all_phases[self.pending_action_number]
        else:
            print('allfezjez',self.all_phases)
            print(action)
            print(self.all_phases[1])
            if (self.all_phases[action] == self.actual_phase):
                self.phase_duration += 1
            else:  # nowa akcja!
                self.phase_duration = 0
                if (self.phase_duration == self.orange_phase_duration):
                    self.actual_phase = self.all_phases[action]
                else:
                    self.actual_phase = self.all_phases[0]  # orange
                    self.pending_action_number = action
        self.t += 1

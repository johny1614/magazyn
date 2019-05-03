import random

class Agent:
    def __init__(self, dic, min_phase_duration,orange_phase_duration=1):
        self.min_phase_duration = min_phase_duration
        self.all_phases = dic['all_phases']
        self.actual_phase = dic['actual_phase'] # sometimes the pending one
        self.real_phase = dic['actual_phase'] # the one changing A matrix
        self.actual_phase_duration = dic['actual_phase_duration']
        self.possible_actions = self.getLocalActionSpace()
        self.orange_phase_duration=orange_phase_duration
        self.t=0

    def getLocalActionSpace(self):
        waitActions = ['wait']
        light_Actions = [1, 2, 3]
        if (self.actual_phase_duration >= self.min_phase_duration):
            return light_Actions
        return waitActions
    def getRandomAction(self):
        return random.choice(self.getLocalActionSpace())
    def modify_A(self, A):
        if (self.actual_phase_duration == 'wait'):
            return
        for manewr in self.real_phase:
            A[manewr] = 1
            print(manewr)
    def pass_action(self,action):
        self.t+=1
        if(not action in self.getLocalActionSpace()):
            print('error with passing wrong action',2/0)
        if(action=='wait' and self.actual_phase_duration<self.orange_phase_duration):
            self.actual_phase_duration+=1
            self.actual_phase=self.all_phases[0] # orange one
        elif(action!=self.actual_phase and not action=='wait'): #zmiana swiatla!
            self.actual_phase=action
            self.real_phase=self.all_phases[0] # ORANGE
            self.actual_phase_duration=0
        elif(action==self.actual_phase or action=='wait'):
            self.actual_phase_duration+=1


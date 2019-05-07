from dataclasses import dataclass

from model.Agent import Agent

class SmartAgent(Agent):
    def __init__(self, dic, min_phase_duration, index, orange_phase_duration=1):
        Agent.__init__(self, dic, min_phase_duration, index, orange_phase_duration=1)
        self.returns = {}
        self.pi = {}
        # Q = {}

        # self.pi = {}
    # def initial_returns():
    #     returns = {}
    #     for s in state_space:
    #         for a_unhashable in action_space:
    #             a = hash_(a_unhashable)
    #             returns[(s, a)] = []
    #     returns

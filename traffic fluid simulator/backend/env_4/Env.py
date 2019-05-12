from typing import List, Tuple

import attr
import numpy as np

from env_data import u, start_A, env_data_x, env_data_A_storage
from model import GlobalState
from model.Action import Action
from model.Agent import Agent
# trojkatne - 3 skrzyzowania, razem 6 drog
from services.globals import Globals
from services.prettyPrinter import pretty_print_A


@attr.s(auto_attribs=True)
class Env:
    agents: List[Agent]
    x = env_data_x
    A_storage = env_data_A_storage

    @property
    def global_state(self) -> GlobalState:
        return tuple(agent.local_state for agent in self.agents)

    @property
    def global_action_space(self) -> Tuple[Action]:
        global_action_space = ()
        for agent in self.agents:
            localSpace = agent.local_action_space()
            global_action_space = global_action_space + (localSpace,)
        return global_action_space

    @property
    def global_reward(self) -> float:
        t = self.t
        return self.x[t][29] + self.x[t][35] + self.x[t][32]

    @property
    def t(self):
        return Globals().time

    @property
    def A(self):
        return self.A_storage[self.t]

    @A.setter
    def A(self, new_A):
        self.A_storage[self.t] = new_A

    def step(self, actions: List[Action]):
        print('actions', actions)
        self.A = start_A()
        self.__pass_actions_to_agents(actions)
        self.__modify_A()
        self.__execute_phase()
        self.__assign_rewards_to_agents()
        print('t', self.t)
        print('x', self.x[self.t])
        print('A', self.A)
        pretty_print_A(self.A)
        Globals().time += 1

    def __execute_phase(self):
        t = self.t
        self.x[t] = np.dot(self.A, self.x[t - 1])
        self.__include_source_cars()
        self.__assign_local_states_to_agents()

    def __assign_rewards_to_agents(self):
        for agent in self.agents:
            agent.assign_reward(previous_x=self.x[self.t - 1], actual_x=self.x[self.t],
                                global_reward=self.global_reward)

    def __pass_actions_to_agents(self, actions: List[Action]):
        for i in range(self.agents.__len__()):
            agent = self.agents[i]
            agent.pass_action(actions[i])

    def __modify_A(self):
        for agent in self.agents:
            self.A = agent.modify_A(self.A)

    def __include_source_cars(self):
        t = self.t
        self.x[t][0] += u[t - 1][0]
        self.x[t][3] += u[t - 1][1]
        self.x[t][6] += u[t - 1][1]

    def __assign_local_states_to_agents(self):
        for agent in self.agents:
            agent.assign_local_state(self.x[self.t])

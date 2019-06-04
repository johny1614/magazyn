from typing import List, Tuple

import attr
import numpy as np

from env_data import u, start_A, env_data_A_storage, max_time, get_x
from model import GlobalState
from model.Agent import Agent
# trojkatne - 3 skrzyzowania, razem 6 drog
from model.Net import Net
from services.globals import Globals

ActionInt = int


def empty_3_list():
    return [[], [], []]


@attr.s(auto_attribs=True)
class Env:
    agents: List[Agent]
    global_rewards: List[float] = attr.Factory(list)
    local_awards: List[List[float]] = attr.Factory(empty_3_list)
    global_memories: List[Net] = attr.Factory(list)

    def __attrs_post_init__(self):
        self.x = get_x()
        self.A = start_A()
        self.cars_out = 0
        self.__assign_local_states_to_agents()

    @property
    def global_state(self) -> GlobalState:
        return tuple(agent.local_state for agent in self.agents)

    @property
    def t(self):
        return Globals().time

    def step(self, actions: List[ActionInt]):
        self.A = start_A()
        self._pass_actions_to_agents(actions)
        self._modify_A()
        self._execute_phase()
        if True or self.t != 0 and self.t != max_time:  # state of 0 is initialized, the last one is not interesting us if  time runs out
            # self.__assign_local_states_to_agents()
            for agent in self.agents:
                agent.remember(self.x[self.t])
            rewards = sum([agent.memories[-1].reward for agent in self.agents])
            self.global_rewards.append(rewards)
        self._count_cars_out()
        self.remember_global_memory()
        Globals().time += 1

    def _execute_phase(self):
        t = self.t
        self.x[t] = np.dot(self.A, self.x[t - 1])
        self.__include_source_cars()

    def _pass_actions_to_agents(self, actions: List[ActionInt]):
        for i in range(self.agents.__len__()):
            agent = self.agents[i]
            agent.pass_action(actions[i])

    def _modify_A(self):
        for agent in self.agents:
            self.A = agent.modify_A(self.A)
        if self.t > 0:
            for i in range(len(self.x[self.t - 1])):
                density = self.x[self.t - 1][i]
                if density > 10:
                    for j in range(len(self.A[:][i])):
                        if j!=i and self.A[j][i]*density>10:
                            A_cell = self.A[j][i]
                            nev_value = 10 / density
                            change = A_cell - nev_value
                            self.A[i][i] += change
                            A_cell = nev_value
                            # print('cell',A_cell)
                            # print('i',i)
                            # print('j',j)
                            self.A[j][i] = A_cell
                            # print('a',self.A[j][i])

    def __include_source_cars(self):
        t = self.t
        self.x[t][0] += u[t - 1][0]
        self.x[t][3] += u[t - 1][1]
        self.x[t][6] += u[t - 1][1]

    def __assign_local_states_to_agents(self):
        for agent in self.agents:
            agent.assign_local_state(self.x[self.t])

    def _count_cars_out(self):
        self.cars_out += self.x[self.t][29]
        self.cars_out += self.x[self.t][32]
        self.cars_out += self.x[self.t][35]

    def remember_global_memory(self):
        net = Net(lights=self.A.tolist(), densities=self.x[self.t].tolist(),rewards=self.global_rewards[self.t])
        self.global_memories.append(net)

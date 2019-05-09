from typing import List, Tuple

import numpy as np
import attr
from env_data import u, start_A, x_size, max_time
from model.Action import Action
from model.Agent import Agent
from model.SaveState import SaveState
from model.LearningState import LearningState

# trojkatne - 3 skrzyzowania, razem 6 drog
from services.globals import Globals


@attr.s(auto_attribs=True)
class Env:
    agents: List[Agent]
    max_time = max_time
    x_size = 36
    x = [x_size * [0]] * max_time
    y = [0] * max_time
    A_storage = [[]] * max_time

    @property
    def t(self):
        return Globals().time

    @property
    def A(self):
        return self.A_storage[self.t]

    @A.setter
    def A(self, new_A):
        self.A_storage[self.t] = new_A

    def step(self, actions):
        Globals().time += 1
        print('time',self.t)
        self.A_storage[self.t] = start_A()
        self.__pass_actions(actions)
        self.__modify_A()
        self.A_storage[self.t] = self.A
        return self.__execute_phase()

    def __execute_phase(self):
        t = self.t
        self.x[t] = np.dot(self.A, self.x[t - 1])
        self.y[t] = self.__calculate_y()
        save_state = SaveState(self.x[t], self.agents, self.A)
        self.__assign_local_states_to_agents()
        return save_state, tuple([agent.local_state for agent in self.agents]), self.y[t]

    def __pass_actions(self, actions):
        for i in range(self.agents.__len__()):
            agent = self.agents[i]
            agent.pass_action(actions[i])

    def get_global_state(self) -> Tuple[LearningState]:
        return tuple(self.agent.local_state for agent in self.agents)

    def get_global_action_space(self) -> Tuple[Action]:
        global_action_space = ()
        for agent in self.agents:
            localSpace = agent.get_local_action_space()
            global_action_space = global_action_space + (localSpace,)
        return global_action_space

    # global_aggregated_densities = global_aggregated_densities + (np.mean([getGroup(den) for den in road]),)

    def __modify_A(self):
        for agent in self.agents:
            self.A = agent.modify_A(self.A)

    def __include_source_cars(self):
        t = self.t
        self.x[t][0] += u[t - 1][0]
        self.x[t][3] += u[t - 1][1]
        self.x[t][6] += u[t - 1][1]

    def __calculate_y(self):
        t = self.t
        return self.x[t][29] + self.x[t][35] + self.x[t][32]

    def __assign_local_states_to_agents(self):
        for agent in self.agents:
            agent.assignLocalState(self.x[self.t])

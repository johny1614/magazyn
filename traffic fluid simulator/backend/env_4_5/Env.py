from typing import List, Tuple

import attr
import numpy as np

import env_data
from env_data import u, start_A, env_data_A_storage, max_time, get_x
from model import GlobalState
from model.Agent import Agent
# trojkatne - 3 skrzyzowania, razem 6 drog
from model.Net import Net, Times
from model.SmartAgent import SmartAgent
from services.globals import Globals

ActionInt = int


def empty_3_list():
    return [[], [], []]


motionTuple = Tuple[float, float]


@attr.s(auto_attribs=True)
class Env:
    agents: List[SmartAgent]
    x: List[List[Tuple[int, int]]] = attr.Factory(get_x)
    global_rewards: List[float] = attr.Factory(list)
    local_awards: List[List[float]] = attr.Factory(empty_3_list)
    global_memories: List[Net] = attr.Factory(list)
    flow_memories: List = attr.Factory(list)
    last_flows: List = attr.Factory(list)
    u = env_data.u

    def __attrs_post_init__(self):
        # self.x = get_x()
        self.A = []
        self.cars_out = 0
        self.__assign_local_states_to_agents()

    @property
    def global_state(self) -> GlobalState:
        return tuple(agent.local_state for agent in self.agents)

    @property
    def t(self):
        return Globals().time

    def step(self, actions: List[ActionInt]):
        for agent in self.agents:
            agent.starting_actual_phase = agent.actual_phase
        self.A.append(start_A())
        self._pass_actions_to_agents(actions)
        self._modify_A()
        # self.update_global_memory_lights()
        Globals().time += 1
        self._execute_phase()
        self.save_motions()
        rewards = self.count_rewards()
        for agent in self.agents:
            agent.remember(densities=self.x[self.t], reward=rewards[agent.index])
        self.global_rewards.append(rewards)
        self._count_cars_out()
        self.remember_global_memory()

    def count_rewards(self):
        rewards = [0] * len(self.agents)
        for flow in self.last_flows:
            rewards[flow['agent_index']] += flow['value']
        return rewards

    def save_motions(self):
        old_time = Globals().time - 1
        new_time = Globals().time
        self.last_flows = []
        for agent in self.agents:
            actual_moves = agent.moves[agent.actual_phase]
            for move in actual_moves:
                A_cell = self.A[Globals().time - 1][move]
                section_from_index = move[1]
                previous_density = self.x[self.t - 1][section_from_index]
                value = A_cell * previous_density
                flow = {'agent_index': agent.index, 'old_time': old_time, 'new_time': new_time, 'move': move,
                        'value': value}
                # print(flow)
                self.last_flows.append(flow)
        for flow in self.last_flows:
            self.flow_memories.append(flow)

    def _execute_phase(self):
        t = self.t
        x_t = np.dot(self.A[t - 1], self.x[t - 1])
        self.x.append(x_t)
        # self.x = np.dot(self.A[t-1], self.x[t - 1])
        self.__include_source_cars()

    def _pass_actions_to_agents(self, actions: List[ActionInt]):
        for i in range(self.agents.__len__()):
            agent = self.agents[i]
            agent.pass_action(actions[i])

    def _modify_A(self):
        t = self.t
        for agent in self.agents:
            self.A[t] = agent.modify_A(self.A[t])
        if self.t > 0:
            for i in range(len(self.x[self.t - 1])):
                density = self.x[self.t][i]
                last_sections = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
                if density > 10 and i in last_sections:
                    for j in range(len(self.A[t][:][i])):
                        if j != i and self.A[t][j][i] * density > 10:
                            A_cell = self.A[t][j][i]
                            new_value = 10 / density
                            change = A_cell - new_value
                            self.A[t][i][i] += change
                            A_cell = new_value
                            self.A[t][j][i] = A_cell

    def __include_source_cars(self):
        t = self.t
        self.x[t][0] += self.u[t - 1][0]
        self.x[t][3] += self.u[t - 1][1]
        self.x[t][6] += self.u[t - 1][1]

    def __assign_local_states_to_agents(self):
        for agent in self.agents:
            agent.assign_local_state(self.x[self.t])

    def _count_cars_out(self):
        self.cars_out += self.x[self.t][29]
        self.cars_out += self.x[self.t][32]
        self.cars_out += self.x[self.t][35]

    # def update_global_memory_lights(self):
    #     if self.t > 0:
    #         lights = self.A[self.t].tolist()  # swiatla
    #         last_index=len(self.global_memories)-1
    #         # self.agents[0].actual_phase
    #         phases = [agent.actual_phase for agent in self.agents]
    #         print(f'dla indeksu {last_index} dajemy swiatla dla faz {phases}')
    #         print('A[21,20]',self.A[self.t][21][20])
    #         print('a',self.A[self.t])
    #         self.global_memories[last_index].lights = lights
    #         print('po akcji jest',self.global_memories[last_index].lights[21][20])
    #         if len(self.global_memories) > 27:
    #             print('nasze 27 ma:',self.global_memories[27].lights[21][20])

    def remember_global_memory(self):
        times = Times(old_time=Globals().time - 1, new_time=Globals().time)
        actions = [agent.action for agent in self.agents]
        rewards = self.global_rewards[self.t - 1]
        densities = self.x[self.t - 1]
        lights = self.A[self.t - 1]
        net = Net(times=times, densities=densities,
                  rewards=rewards,
                  actions=actions,
                  lights=lights)
        self.global_memories.append(net)

    def update_global_memory_rewards(self):
        for i in range(len(self.global_memories)):
            net = self.global_memories[i]
            net.rewards = [agent.memories[i].reward for agent in self.agents]
# @attr.s(auto_attribs=True)
# class GlobalMemory:
#

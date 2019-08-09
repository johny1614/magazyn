from typing import List, Tuple

import attr
import numpy as np

import env_settings
from Utils import empty_3_list
from env_settings import start_A, get_x
from model import GlobalState
from model.Action import ActionInt
from model.LearningState import LearningState
from model.Net import Net, Times
from model.SmartAgent import SmartAgent
from services.globals import Globals


@attr.s(auto_attribs=True)
class Env:
    agents: List[SmartAgent]
    x: List[List[Tuple[int, int]]] = attr.Factory(get_x)
    global_rewards: List[float] = attr.Factory(list)
    local_awards: List[List[float]] = attr.Factory(empty_3_list)
    global_memories: List[Net] = attr.Factory(list)
    flow_memories: List = attr.Factory(list)
    last_flows: List = attr.Factory(list)
    u = env_settings.u

    def assign_state(self, state: LearningState):
        for agent in self.agents:
            agent.orange_phase_duration = state.orange_phase_duration
            agent.actual_phase = state.actual_phase
            agent.starting_actual_phase = state.starting_actual_phase
            agent.phase_duration = state.phase_duration
            self.x[self.t] = state.densities

    def __attrs_post_init__(self):
        Globals().time = 0
        self.A = []
        self.cars_out = 0
        self.assign_local_states_to_agents()

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
        self.remember_memory()

    def count_summed_rewards(self) -> Tuple[int, int]:
        memsum = 0
        i = 0
        for agent in self.agents:
            for mem in agent.memories:
                i += 1
                memsum += mem.reward
        return memsum, memsum / i

    def count_rewards(self):
        # TODO to na pewno jest ok?
        rewards = [0] * len(self.agents)
        for flow in self.last_flows:
            rewards[flow['agent_index']] += flow['value']
        return rewards

    def save_motions(self):
        old_time = Globals().time - 1
        new_time = Globals().time
        self.last_flows = []
        for agent in self.agents:
            actual_moves = () if agent.actual_phase == 'orange' else agent.moves[agent.actual_phase]
            for move in actual_moves:
                if move[0] == 404:
                    continue
                A_cell = self.A[Globals().time - 1][move]
                section_from_index = move[1]
                previous_density = self.x[self.t - 1][section_from_index]
                value = A_cell * previous_density
                flow = {'agent_index': agent.index, 'old_time': old_time, 'new_time': new_time, 'move': move,
                        'value': value}
                self.last_flows.append(flow)
        self.flow_memories.append(self.last_flows)

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
        # print('modify A t',t)
        # print('x',self.x[t])
        for agent in self.agents:
            self.A[t] = agent.modify_A(self.A[t])
        if self.t > 0:
            for i in range(len(self.x[self.t - 1])):
                density = self.x[self.t][i]
                if density > 10 and i in env_settings.not_last_sections:
                    for j in range(len(self.A[t][:][i])):
                        if j != i and self.A[t][j][i] * density > 10:
                            A_cell = self.A[t][j][i]
                            new_value = 10 / density
                            change = A_cell - new_value
                            self.A[t][i][i] += change
                            A_cell = new_value
                            self.A[t][j][i] = A_cell
        # print(self.A[t])

    def __include_source_cars(self):
        t = self.t
        self.x[t][0] += self.u[t - 1][0]
        self.x[t][2] += self.u[t - 1][1]

    def assign_local_states_to_agents(self):
        for agent in self.agents:
            agent.assign_local_state(self.x[self.t])

    def _count_cars_out(self):
        self.cars_out += self.x[self.t][3]
        self.cars_out += self.x[self.t][5]

    def remember_memory(self):
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

    # def update_memory_rewards(self):
    # we dont need it. It makes a mistake that from 0th episode it s only taken. Not deleted yet couse always it was here!
    #     i=0
    #     for mem in self.agents[0].memories:
    #         print(f'{i} mem agent {mem}')
    #         i+=1
    #     for i in range(len(self.global_memories)):
    #         net = self.global_memories[i]
    #         net.rewards = [agent.memories[i].reward for agent in self.agents]

    def deepCopy(self):
        copied_agents = [agent.deep_copy() for agent in self.agents]
        new_env = Env(copied_agents)
        new_env.__dict__ = self.__dict__.copy()  # just a shallow copy
        new_env.agents = copied_agents
        return new_env

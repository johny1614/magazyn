from typing import List, Tuple
import attr
import numpy as np
import env_settings
from Utils import empty_3_list
from env_settings import start_A, get_x
from model import GlobalState
from model.Action import ActionInt, yellow
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

    def assign_state(self, state: LearningState):
        for agent in self.agents:
            agent.yellow_phase_duration = state.yellow_phase_duration
            agent.actual_phase = state.actual_phase
            agent.starting_actual_phase = state.starting_actual_phase
            agent.phase_duration = state.phase_duration
            self.x[self.t] = state.densities

    def __attrs_post_init__(self):
        Globals().time = 0
        max_time = Globals().vp.max_time_greedy
        self.u = Globals().get_u(max_time)
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

    def count_rewards_negative(self):
        rewards = [0] * len(self.agents)
        for i in range(len(self.agents)):
            agent=self.agents[i]
            for sec in agent.local_phase_sections:
                rewards[i]-=self.global_state[0].densities[sec]
        return rewards

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
            actual_moves = () if agent.actual_phase == yellow else agent.moves[agent.actual_phase]
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
                if density > 10 and i in env_settings.not_last_sections:
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
        i = 0
        for source_section in env_settings.source_sections:
            self.x[t][source_section] += self.u[t - 1][i]
            i += 1

    def assign_local_states_to_agents(self):
        for agent in self.agents:
            agent.assign_local_state(self.x[self.t])

    def _count_cars_out(self):
        cars_out = 0
        for sec in env_settings.last_sections:
            cars_out += self.x[self.t][sec]
        Globals().cars_out_memory.append(cars_out)
        self.cars_out += cars_out

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

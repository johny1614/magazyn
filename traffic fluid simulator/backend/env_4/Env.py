import numpy as np

from env_data import u, start_A, x_size, max_time
from model.SaveState import SaveState

# trojkatne - 3 skrzyzowania, razem 6 drog
from services.agentFactory import get_Agents


class Env:
    def __init__(self,agents):
        self.agents = agents
        self.max_time = max_time
        self.x_size = x_size
        self.x = [self.x_size * [0]] * max_time
        self.y = [0] * max_time
        self.A_storage = [[]] * max_time
        self.t = 0
        self.A = None

    def step(self, actions):
        self.t += 1
        self.A = start_A()
        self.__pass_actions(actions)
        self.__modify_A()
        self.A_storage[self.t] = self.A
        self.__execute_phase()
        return self.__execute_phase()

    def get_global_action_space(self):
        global_action_space = []
        for agent in self.agents:
            localSpace = agent.getLocalActionSpace()
            global_action_space.append(localSpace)
        return global_action_space

    def __modify_A(self):
        for agent in self.agents:
            self.A = agent.modify_A(self.A)

    def __execute_phase(self):
        t = self.t
        self.x[t] = np.dot(self.A, self.x[t - 1])
        self.x[t][0] += u[t - 1][0]
        self.x[t][3] += u[t - 1][1]
        self.x[t][6] += u[t - 1][1]
        self.y[t] = self.x[t][29] + self.x[t][35] + self.x[t][32]
        save_state = SaveState(self.x[t], self.agents, self.A)
        self.__assign_local_states_to_agents()
        return save_state, [agent.local_state for agent in self.agents], self.y[t]

    def __assign_local_states_to_agents(self):
        for agent in self.agents:
            agent.assignLocalState(self.x[self.t])

    def __pass_actions(self, actions):
        for i in range(self.agents.__len__()):
            agent = self.agents[i]
            agent.pass_action(actions[i])

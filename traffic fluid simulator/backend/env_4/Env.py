import numpy as np

from model.GlobalState import GlobalState
from env_data import u, start_A, get_Agents, x_size, max_time


# trojkatne - 3 skrzyzowania, razem 6 drog

class Env:
    def __init__(self):
        self.max_time = max_time
        self.x_size = x_size
        self.agents = get_Agents()
        self.x = [self.x_size * [0]] * max_time
        self.y = [0] * max_time
        self.A_storage = [[]] * (max_time)
        self.t = 0


    def step(self, actions):
        self.t += 1
        self.A=start_A()
        self.__pass_actions(actions)
        self.__modify_A()
        self.A_storage[self.t ] = self.A
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
        global_state = GlobalState(self.x[t], self.agents, self.A)
        return global_state, self.y[t]

    def __pass_actions(self, actions):
        for i in range(self.agents.__len__()):
            agent = self.agents[i]
            agent.pass_action(actions[i])

import os
import sys
import copy
from copy import deepcopy

import numpy as np
from matplotlib.pyplot import plot
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.optimizers import Adam
from tensorflow.python.keras import regularizers
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.getcwd()))

from services.dryRunnerService import dry_run
import unittest
from typing import List
import env_settings
from Env import Env
from model import SmartAgent
from model.ExportData import ExportData
from services.agentFactory import get_SmartAgents
from services.globals import Globals

orange = 'orange'


def get_agents_env():
    agents = get_SmartAgents()
    env = Env(agents)
    return agents, env


class Testing(unittest.TestCase):
    def test_no_1_000_then_111(self):
        # Testujemy dla akcji ktora rzeczywiscie byla i powinno przewidziec bardzo dobrze
        agents: List[SmartAgent] = get_SmartAgents()
        env = Env(agents)
        env.u = env_settings.u_all_2
        max_time = 15
        Globals().time = 0
        for t in range(max_time):
            actions = [0, 0, 0]
            if t == 60 or t >= 63:
                actions = [1, 1, 1]
            if t == 61 or t == 62 or t == 1 or t == 2:
                actions = [orange, orange, orange]
            env.step(actions)
            if t == 10:
                dry_run(env, env.agents, [1, 2, 1])
        for agent in agents:
            agent.reshape_rewards()

        # exportData = ExportData(learningMethod='DQN', learningEpochs=0, nets=env.global_memories,
        #                         netName='net4',
        #                         densityName='test_dry_runner_no_1')
        # exportData.saveToJson()


if __name__ == '__main__':
    unittest.main()

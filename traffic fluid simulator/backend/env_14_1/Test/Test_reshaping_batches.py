import os
import random
import sys

import numpy as np
from matplotlib.pyplot import plot
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.optimizers import Adam
from tensorflow.python.keras import regularizers
import matplotlib.pyplot as plt
sys.path.append(os.path.dirname(os.getcwd()))

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
    def test_no_1_actions_0_1_what_is_terrible_idea(self):
        agents: List[SmartAgent] = get_SmartAgents()
        for agent in agents:
            agent.model = agent._build_model(layers=[20, 50, 30, 18])
        env = Env(agents)
        env.u = env_settings.u_all_2
        max_time = 90
        Globals().time = 0
        for t in range(max_time):
            actions = [0]
            if t == 60 or t >= 63:
                actions = [1]
            if t == 61 or t == 62:
                actions = [orange]
            env.step(actions)
        for agent in agents:
            agent.reshape_rewards()
        exportData = ExportData(learningMethod='DQN', learningEpochs=0, nets=env.global_memories,
                                netName='net4',
                                densityName='test_learn_no_1')
        exportData.saveToJson()
        agents[0].train_full(epochs=15000, learning_rate=0.001)
        x = [4,4,0]
        predictions = agents[0].model.predict(np.array([x]))
        self.assertTrue(predictions[0][0]>predictions[0][1])

if __name__ == '__main__':
    unittest.main()

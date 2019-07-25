import os
import sys

import numpy as np
from matplotlib.pyplot import plot
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.optimizers import Adam
from tensorflow.python.keras import regularizers
import matplotlib.pyplot as plt

from random_epochs_generator import epoch

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
    def test_no_1_(self):
        epochs = range(1)
        xy_20_all = []
        for e in epochs:
            agents: List[SmartAgent] = get_SmartAgents()
            Globals().epsilon = 1
            env: Env = epoch(agents)
            env.u = env_settings.u_all_2
            for agent in env.agents:
                agent.reshape_rewards()
            env.update_memory_rewards()
            env.remember_memory()


if __name__ == '__main__':
    unittest.main()

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

from random_epochs_generator import generate_random_epochs
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
    # def test_no_0_reshape_future_2(self):
    #     for vp in Globals().val_params:
    #         vp.reshape_future = 2
    #     agents: List[SmartAgent] = get_SmartAgents()
    #     env = Env(agents)
    #     env.u = env_settings.u_all_2
    #     max_time = 90
    #     Globals().time = 0
    #     for t in range(max_time):
    #         actions = [0]
    #         env.step(actions)
    #     for agent in agents:
    #         agent.reshape_rewards()
    #     self.assertEquals(agents[0].memories[0].reward,2)
    #     self.assertEquals(agents[0].memories[1].reward,4)
    #     for i in range(2,88):
    #         self.assertEquals(agents[0].memories[i].reward,6)
    #     exportData = ExportData(learningMethod='DQN', learningEpochs=0, nets=env.global_memories,
    #                             netName='net14',
    #                             densityName='test_reshaping_no_0')
    #     exportData.saveToJson()
    #
    # def test_no_1_reshape_future_5(self):
    #     for vp in Globals().val_params:
    #         vp.reshape_future = 5
    #     agents: List[SmartAgent] = get_SmartAgents()
    #     env = Env(agents)
    #     env.u = env_settings.u_all_2
    #     max_time = 90
    #     Globals().time = 0
    #     for t in range(max_time):
    #         actions = [0]
    #         env.step(actions)
    #     for agent in agents:
    #         agent.reshape_rewards()
    #     self.assertEquals(agents[0].memories[0].reward, 8)
    #     self.assertEquals(agents[0].memories[1].reward, 10)
    #     for i in range(2, 85):
    #         self.assertEquals(agents[0].memories[i].reward, 12)
    #     exportData = ExportData(learningMethod='DQN', learningEpochs=0, nets=env.global_memories,
    #                             netName='net14',
    #                             densityName='test_reshaping_no_1')
    #     exportData.saveToJson()
    #
    # def test_no_2_reshape_future_2_times(self):
    #     for vp in Globals().val_params:
    #         vp.reshape_future = 2
    #     agents: List[SmartAgent] = get_SmartAgents()
    #     env = Env(agents)
    #     env.u = env_settings.u_all_2
    #     max_time = 90
    #     Globals().time = 0
    #     for t in range(max_time):
    #         actions = [0]
    #         env.step(actions)
    #     for agent in agents:
    #         agent.reshape_rewards()
    #     self.assertEquals(agents[0].memories[0].reward, 2)
    #     self.assertEquals(agents[0].memories[1].reward, 4)
    #     for i in range(2, 88):
    #         self.assertEquals(agents[0].memories[i].reward, 6)
    #     for i in range(88, 90):
    #         self.assertEquals(agents[0].memories[i].learn_usable, False)
    #     exportData = ExportData(learningMethod='DQN', learningEpochs=0, nets=env.global_memories,
    #                             netName='net14',
    #                             densityName='test_reshaping_no_2')
    #     exportData.saveToJson()
    #     # nastepny epoch przy tym samym agencie
    #     Globals().actual_epoch_index += 1
    #     env = Env(agents)
    #     env.u = env_settings.u_all_2
    #     max_time = 90
    #     Globals().time = 0
    #     for t in range(max_time):
    #         actions = [0]
    #         env.step(actions)
    #     for agent in agents:
    #         agent.reshape_rewards()
    #     # sprawdzamy czy starych nie zmienil przypadkiem
    #     self.assertEquals(agents[0].memories[0].reward, 2)
    #     self.assertEquals(agents[0].memories[1].reward, 4)
    #     for i in range(2, 88):
    #         self.assertEquals(agents[0].memories[i].reward, 6)
    #     for i in range(88, 90):
    #         self.assertEquals(agents[0].memories[i].learn_usable, False)
    #     # i teraz te nowe
    #     self.assertEquals(agents[0].memories[90].reward, 2)
    #     self.assertEquals(agents[0].memories[91].reward, 4)
    #     for i in range(92, 178):
    #         self.assertEquals(agents[0].memories[i].reward, 6)
    #     for i in range(178, 180):
    #         self.assertEquals(agents[0].memories[i].learn_usable, False)

    def test_no_3_reshape_future_many_times_are_rewards_ok(self):
        # TRZEBA USTAWIC:
        # if state.actual_phase == 'orange':
        #     return 'orange'
        # return 0
        # w metodzie get_action - wtedy ma przechodzic test
        Globals().reshape_future = 4
        agents=generate_random_epochs(learntAgents=False,epochs=range(50),u=env_settings.u_all_2)  # bierze nowych agentow i tu jest 'is'
        rewards = [mem.reward for mem in agents[0].memories]
        a=14







if __name__ == '__main__':
    unittest.main()

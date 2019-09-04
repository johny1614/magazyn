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
    # def test_no_1_actions_0_1_what_is_terrible_idea(self):
    #     agents: List[SmartAgent] = get_SmartAgents()
    #     for agent in agents:
    #         agent.model = agent._build_model(layers=[20, 50, 30, 18])
    #     env = Env(agents)
    #     env.u = env_settings.u_all_2
    #     max_time = 90
    #     Globals().time = 0
    #     for t in range(max_time):
    #         actions = [0]
    #         if t == 60 or t >= 63:
    #             actions = [1]
    #         if t == 61 or t == 62:
    #             actions = [orange]
    #         env.step(actions)
    #     for agent in agents:
    #         agent.reshape_rewards()
    #     exportData = ExportData(learningMethod='DQN', learningEpochs=0, nets=env.global_memories,
    #                             netName='net4',
    #                             densityName='test_learn_no_1')
    #     exportData.saveToJson()
    #     agents[0].train_full(epochs=15000, learning_rate=0.001)
    #     x = [4,4,0]
    #     predictions = agents[0].model.predict(np.array([x]))
    #     self.assertTrue(predictions[0][0]>predictions[0][1])

    # def test_no_2_actions_random_no_crashes(self):
    #     agents: List[SmartAgent] = get_SmartAgents()
    #     for agent in agents:
    #         agent.model = agent._build_model(layers=[20, 50, 30, 18])
    #     env = Env(agents)
    #     env.u = env_settings.u_all_2
    #     max_time = 90
    #     Globals().time = 0
    #     for t in range(max_time):
    #         actions=[]
    #         actions.append(random.choice(agents[0].local_action_space))
    #         # print(f't:{t} actions: {agents[0].local_action_space}, chosen_action:{actions[0]}')
    #         env.step(actions)
    #     for agent in agents:
    #         agent.reshape_rewards()
    #     exportData = ExportData(learningMethod='DQN', learningEpochs=0, nets=env.global_memories,
    #                             netName='net4',
    #                             densityName='test_learn_no_2')
    #     exportData.saveToJson()
    #     agents[0].train_full(epochs=15000, learning_rate=0.001)
    #     x = [4, 4, 0]
    #     predictions = agents[0].model.predict(np.array([x]))
    #
    #     def test_no_3_actions_random_30s_he_predicts_0_phases_well(self):
    #         agents: List[SmartAgent] = get_SmartAgents()
    #         for agent in agents:
    #             agent.model = agent._build_model(layers=[20, 50, 30, 18])
    #         env = Env(agents)
    #         env.u = env_settings.u_all_2
    #         max_time = 90
    #         Globals().time = 0
    #         for t in range(max_time):
    #             actions = []
    #             actions.append(random.choice(agents[0].local_action_space))
    #             # print(f't:{t} actions: {agents[0].local_action_space}, chosen_action:{actions[0]}')
    #             env.step(actions)
    #         for agent in agents:
    #             agent.reshape_rewards()
    #         exportData = ExportData(learningMethod='DQN', learningEpochs=0, nets=env.global_memories,
    #                                 netName='net4',
    #                                 densityName='test_learn_no_2')
    #         exportData.saveToJson()
    #         agents[0].train_full(epochs=15000, learning_rate=0.001)
    #         x = [4, 4, 0]
    #         predictions = agents[0].model.predict(np.array([x]))

        # similar state but predictions ho crazy!!! overfiting as hecc
    # def test_no_2_000_then_111_what_is_brilliant_idea(self):
    #     # Testujemy dla stanu ktory raz sie pojawil, ale takze dla bardzo podobnego - i chcemy podobnego wyniku
    #     # aby nie bylo overfittingu
    #     act_preds_1_reg = []
    #     close_preds_1_reg = []
    #     agents: List[SmartAgent] = get_SmartAgents()
    #     for agent in agents:
    #         model = Sequential()
    #         model.add(Dense(13, input_dim=10, activation='relu'))  # 1st hidden layer; states as input
    #         # model.add(Dense(8, activation='relu'))
    #         model.add(Dense(8, activation='relu', kernel_regularizer=regularizers.l2(0.5)))
    #         model.add(Dense(3, activation='linear'))
    #         model.compile(loss='mse',
    #                       optimizer=Adam())
    #         agent.model = model
    #
    #     env = Env(agents)
    #     env.u = env_settings.u_all_2
    #     max_time = 90
    #     Globals().time = 0
    #     for t in range(max_time):
    #         # actions = [1, 1, 1] if t < 60 elif 60 == t [2, 2, 2]
    #         actions = [0, 0, 0]
    #         if t == 60 or t >= 63:
    #             actions = [1, 1, 1]
    #         if t == 61 or t == 62:
    #             actions = [orange, orange, orange]
    #         env.step(actions)
    #     for agent in agents:
    #         agent.reshape_rewards()
    #     i = 0
    #     epochs = 5
    #     a = True
    #     while a:
    #         i += epochs
    #         agents[0].train(batch_size=40, epochs=epochs, learning_rate=0.001)
    #         x = [2, 2, 2] + [0.6, 0.6, 28.88] + [0.126, 0.126, 0.18] + [0]
    #         predictions_actual = agents[0].model.predict(np.array([x]))
    #         x = [0, 0, 0] + [0, 0, 29] + [0, 0, 0] + [1]
    #         predictions_close = agents[0].model.predict(np.array([x]))
    #         act_preds_1_reg.append(predictions_actual[0][1])
    #         close_preds_1_reg.append(predictions_close[0][1])
    #         print(f'{i},actual: {predictions_actual} close: {predictions_close}')
    #         if i == 6000:
    #             a = False
    #     plt.plot(act_preds_1_reg,color='blue')
    #     plt.plot(close_preds_1_reg,color='green')
    #     # plt.ylabel('some numbers')
    #     # plt.show()

        # #NOT REGULIZED
        # act_preds_1 = []
        # close_preds_1 = []
        # agents: List[SmartAgent] = get_SmartAgents()
        # for agent in agents:
        #     model = Sequential()
        #     model.add(Dense(13, input_dim=10, activation='relu'))  # 1st hidden layer; states as input
        #     model.add(Dense(8, activation='relu'))
        #     model.add(Dense(3, activation='linear'))
        #     model.compile(loss='mse',
        #                   optimizer=Adam())
        #     agent.model = model
        #
        # Globals().time = 0
        # env = Env(agents)
        # env.u = env_settings.u_all_2
        # max_time = 90
        # for t in range(max_time):
        #     # actions = [1, 1, 1] if t < 60 elif 60 == t [2, 2, 2]
        #     actions = [0, 0, 0]
        #     if t == 60 or t >= 63:
        #         actions = [1, 1, 1]
        #     if t == 61 or t == 62:
        #         actions = [orange, orange, orange]
        #     env.step(actions)
        # for agent in agents:
        #     agent.reshape_rewards()
        # i = 0
        # epochs = 20
        # a = True
        # while a:
        #     i += epochs
        #     agents[0].train(batch_size=40, epochs=epochs, learning_rate=0.001)
        #     x = [2, 2, 2] + [0.6, 0.6, 28.88] + [0.126, 0.126, 0.18] + [0]
        #     predictions_actual = agents[0].model.predict(np.array([x]))
        #     x = [0, 0, 0] + [0, 0, 29] + [0, 0, 0] + [1]
        #     predictions_close = agents[0].model.predict(np.array([x]))
        #     act_preds_1.append(predictions_actual[0][1])
        #     close_preds_1.append(predictions_close[0][1])
        #     print(f'{i},actual: {predictions_actual} close: {predictions_close}')
        #     if i == 40000:
        #         a = False
        # plt.plot(close_preds_1,color='yellow')
        # plt.plot(act_preds_1,color='orange')
        # plt.show()


    # def test_no_5_actions_0_1_what_is_terrible_idea(self):
    #     agents: List[SmartAgent] = get_SmartAgents()
    #     for agent in agents:
    #         agent.model = agent._build_model(layers=[20, 50, 30, 18])
    #     env = Env(agents)
    #     env.u = env_settings.u_all_2
    #     max_time = 90
    #     Globals().time = 0
    #     for t in range(max_time):
    #         actions = [0]
    #         # if t == 60 or t >= 63:
    #         #     actions = [1]
    #         # if t == 61 or t == 62:
    #         #     actions = [orange]
    #         # env.step(actions)
    #     for agent in agents:
    #         agent.reshape_rewards()
    #     # exportData = ExportData(learningMethod='DQN', learningEpochs=0, nets=env.global_memories,
    #     #                         netName='net4',
    #     #                         densityName='test_learn_no_1')
    #     # exportData.saveToJson()
    #     while True:
    #         agents[0].train_full(epochs=15000, learning_rate=0.001)
    #     x = [4,4,0]
    #     predictions = agents[0].model.predict(np.array([x]))
    #     self.assertTrue(predictions[0][0]>predictions[0][1])
    #
    #
    #






        #      Jest dobrze przez pewien czas, ale potem sie psuje

        # similar state but predictions ho crazy!!! overfiting as hecc

        # exportData = ExportData(learningMethod='DQN', learningEpochs=0, nets=env.global_memories,
        #                         netName='net4',
        #                         densityName='test_learn_no_2')
        # exportData.saveToJson()


if __name__ == '__main__':
    unittest.main()

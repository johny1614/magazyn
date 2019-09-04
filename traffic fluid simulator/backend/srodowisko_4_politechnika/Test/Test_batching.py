import os
import sys

import numpy as np
from tensorflow.python import keras
from tensorflow.python.keras.optimizers import Adam

sys.path.append(os.path.dirname(os.getcwd()))
import matplotlib.pyplot as plt
from services.globals import Globals

from Env import Env

import env_settings

from model.LearningState import LearningState

from model.ExportData import ExportData

from nn_trainer import get_batches, train

from random_epochs_generator import save_batches, generate_random_epochs

from fixed_env_flow import single_simulate, simulate_from_env
import unittest
from services.agentFactory import get_SmartAgents

orange = 'orange'


class Testing(unittest.TestCase):
    # def test_no_0_some_batch_data(self):
    #     generate_random_epochs(save_front_json=True, epochs=range(1))
    # def test_no_1(self):
    #     agents = get_SmartAgents()
    #     for agent in agents:
    #         agent.orange_phase_duration=2
    #         agent.actual_phase=0
    #         agent.starting_actual_phase=0
    #     action_1=[1]
    #     action_0=[0]
    #     env=Env(agents)
    #     simulate_from_env(env,action_0)
    #     simulate_from_env(env,action_0)
    #     simulate_from_env(env,action_0)
    #     simulate_from_env(env,action_0)
    #     simulate_from_env(env,action_0)
    #     simulate_from_env(env,action_1) # t=5
    #     simulate_from_env(env,[orange])
    #     simulate_from_env(env,[orange])
    #     simulate_from_env(env,action_1)
    #     simulate_from_env(env,action_1)
    #     simulate_from_env(env,action_1)
    #     simulate_from_env(env,action_0) # t=10
    #     simulate_from_env(env,[orange])
    #     simulate_from_env(env,[orange])
    #     memories = env.global_memories
    #     self.assertEqual(agents[0].memories[5].holded_lights,False)
    #     self.assertEqual(agents[0].memories[10].holded_lights,False)
    #     exportData = ExportData(learningMethod='DQN', learningEpochs=0, nets=memories,
    #                             netName='net14',
    #                             densityName='test_batching_1')
    #     exportData.saveToJson()
    #     a=23

    # def test_no_2_batch_create(self):
    #     agents = get_SmartAgents()
    #     for agent in agents:
    #         agent.orange_phase_duration = 2
    #         agent.actual_phase = 0
    #         agent.starting_actual_phase = 0
    #     action_1 = [1]
    #     action_0 = [0]
    #     env = Env(agents)
    #     for x in range(50):
    #         simulate_from_env(env, action_0)
    #     simulate_from_env(env, action_1)  # t=5
    #     simulate_from_env(env, [orange])
    #     simulate_from_env(env, [orange])
    #     for x in range(10):
    #         simulate_from_env(env, action_1)
    #     memories = env.global_memories
    #     save_batches(agents)
    #     batches = get_batches()
    #     # dla memory 50 powinno byc value dla akcji 1 rowne Q=0*gamma+0*gamma+10*gamma^2+gamma^3*przewidywania sieci
    #     # dla gamma =0.9 jest to przynajmniej 8.1
    #     print('valu akcji',batches[0]['y_batch'][50][1])
    #     # self.assertEqual(batches[0]['y_batch'][50][1])
    #     exportData = ExportData(learningMethod='DQN', learningEpochs=0, nets=memories,
    #                             netName='net14',
    #                             densityName='test_batching_2')
    #     exportData.saveToJson()
    #     a=324

    # def test_no_3_batch_create(self):
    #     agents = get_SmartAgents()
    #     for agent in agents:
    #         agent.orange_phase_duration = 2
    #         agent.actual_phase = 0
    #         agent.starting_actual_phase = 0
    #     action_1 = [1]
    #     action_0 = [0]
    #     env = Env(agents)
    #     simulate_from_env(env, action_0) # t=0
    #     simulate_from_env(env, action_1) # t=1
    #     simulate_from_env(env, [orange]) # t=2
    #     simulate_from_env(env, [orange]) # t=3
    #     simulate_from_env(env, action_1) # t=4
    #     simulate_from_env(env, action_0) # t=5
    #     simulate_from_env(env, [orange]) # t=6
    #     simulate_from_env(env, [orange]) # t=7
    #     for x in range(30):
    #         simulate_from_env(env, action_0)  # t=6
    #     self.assertEqual(env.agents[0].memories[0].state.starting_actual_phase,0)
    #     self.assertEqual(env.agents[0].memories[0].state.actual_phase,0)
    #     self.assertEqual(env.agents[0].memories[0].action,0)
    #
    #     self.assertEqual(env.agents[0].memories[1].state.starting_actual_phase,0)
    #     self.assertEqual(env.agents[0].memories[1].state.actual_phase,orange)
    #     self.assertEqual(env.agents[0].memories[1].action,1)
    #
    #     self.assertEqual(env.agents[0].memories[2].state.starting_actual_phase,orange)
    #     self.assertEqual(env.agents[0].memories[2].state.actual_phase,orange)
    #     self.assertEqual(env.agents[0].memories[2].action,orange)
    #
    #     self.assertEqual(env.agents[0].memories[3].state.starting_actual_phase,orange)
    #     self.assertEqual(env.agents[0].memories[3].state.actual_phase,1)
    #     self.assertEqual(env.agents[0].memories[3].action,orange)
    #
    #     self.assertEqual(env.agents[0].memories[4].state.starting_actual_phase,1)
    #     self.assertEqual(env.agents[0].memories[4].state.actual_phase,1)
    #     self.assertEqual(env.agents[0].memories[4].action,1)
    #
    #     self.assertEqual(env.agents[0].memories[5].state.starting_actual_phase, 1)
    #     self.assertEqual(env.agents[0].memories[5].state.actual_phase, orange)
    #     self.assertEqual(env.agents[0].memories[5].action, 0)
    #
    #     self.assertEqual(env.agents[0].memories[6].state.starting_actual_phase, orange)
    #     self.assertEqual(env.agents[0].memories[6].state.actual_phase, orange)
    #     self.assertEqual(env.agents[0].memories[6].action, orange)
    #     save_batches(agents)
    #
    #     exportData = ExportData(learningMethod='DQN', learningEpochs=0, nets=env.global_memories,
    #                             netName='net14',
    #                             densityName='test_batching_3')
    #     exportData.saveToJson()
    #     a = 324
    #

    def test_no_4_batch_create(self):
        agents = get_SmartAgents()
        j = 1
        predictions = []
        while True:
            j += 1
            for agent in agents:
                agent.orange_phase_duration = 2
                agent.actual_phase = 0
                agent.starting_actual_phase = 0
                agent.memories = []
            action_1 = [1]
            action_0 = [0]
            env = Env(agents)
            for i in range(100):
                simulate_from_env(env, action_0)  # t=0
            for i in range(50):
                simulate_from_env(env, action_1)  # t=0
            exportData = ExportData(learningMethod='DQN', learningEpochs=0, nets=env.global_memories,
                                    netName='net14',
                                    densityName='test_batching_4')
            exportData.saveToJson()
            save_batches(agents)
            # train(agents=agents)
            pred = agents[0].model.predict(np.array([[3, 3, 3, 297, 1, 0]]))
            predictions.append(pred)
            batches = agents[0].full_batch_no_orange()
            agents[0].model.fit(np.array(batches[0]),np.array(batches[1]),epochs=1000,validation_split=0)
            a = 435
            ########### THAT IS OK
            # model = keras.models.Sequential()
            # model.add(keras.layers.Dense(7, activation='relu', input_dim=5))
            # model.add(keras.layers.Dense(12, activation='relu'))
            # model.add(keras.layers.Dense(10, activation='relu'))
            # model.add(keras.layers.Dense(2))
            # model.compile(loss='mse', optimizer=Adam())
            # y=batches[1]
            # model.fit(np.array(batches[0]),np.array(batches[1]),epochs=1,validation_split=0)
            # predictions=model.predict(np.array(batches[0]))
            # diffs = [(predictions[i] - y[i]) ** 2 for i in range(len(predictions))]
            # mse = sum(sum(diffs)) / len(predictions) / len(predictions[0])
            # print('mse',mse)
            ###########
            name = 'pred.png'
            plt.plot([pred[0][0] for pred in predictions], label='0')
            plt.plot([pred[0][1] for pred in predictions], label='1')
            plt.legend()
            plt.savefig(name)
            plt.close()


if __name__ == '__main__':
    unittest.main()

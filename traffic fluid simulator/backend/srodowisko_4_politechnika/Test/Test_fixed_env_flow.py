import os
import sys

import numpy as np

sys.path.append(os.path.dirname(os.getcwd()))
import matplotlib.pyplot as plt

from Env import Env

import env_settings

from model.LearningState import LearningState

from model.ExportData import ExportData

from nn_trainer import get_batches, train

from random_epochs_generator import save_batches

from fixed_env_flow import single_simulate, simulate_from_env
import unittest
from services.agentFactory import get_SmartAgents

orange = 'orange'


class Testing(unittest.TestCase):
    # def test_no_0_phase_0_action_1(self):
    #     agents = get_SmartAgents()
    #     actual_phase = 0
    #     orange_phase_duration = 2
    #     phase_duration = orange_phase_duration + 1
    #     den = [0, 5, 10, 2]
    #     action = [1]
    #     env = single_simulate(agents, actual_phase, phase_duration, den, orange_phase_duration=orange_phase_duration,
    #                           actions=action)
    #     self.assertEqual(agents[0].actual_phase, orange)
    #
    # def test_no_1_phase_0_action_1_orange_until_phase_1(self):
    #     agents = get_SmartAgents()
    #     agents[0].pending_phase = None
    #     actual_phase = 0
    #     orange_phase_duration = 2
    #     phase_duration = orange_phase_duration + 1  # bysmy mogli od razu przelaczyc
    #     den = [0, 5, 10, 2]
    #     action = [1]
    #     env = single_simulate(agents, actual_phase, phase_duration, den, orange_phase_duration=orange_phase_duration,
    #                           actions=action)
    #     self.assertEqual(agents[0].actual_phase, orange)
    #     simulate_from_env(env, actions=[orange])
    #     simulate_from_env(env, actions=[orange])
    #     self.assertEqual(agents[0].actual_phase, 1)
    #
    # def test_no_2_phase_0_action_1_orange_until_phase_1_orange_phase_duration_4(self):
    #     agents = get_SmartAgents()
    #     actual_phase = 0
    #     orange_phase_duration = 4
    #     phase_duration = orange_phase_duration + 1  # bysmy mogli od razu przelaczyc
    #     den = [0, 5, 10, 2]
    #     action = [1]
    #     env = single_simulate(agents, actual_phase, phase_duration, den,
    #                           orange_phase_duration=orange_phase_duration, actions=action)
    #     self.assertEqual(agents[0].actual_phase, orange)  # 1 raz orange
    #     env = simulate_from_env(env, actions=[orange])
    #     self.assertEqual(agents[0].actual_phase, orange)  # 2 raz orange
    #     env = simulate_from_env(env, actions=[orange])
    #     self.assertEqual(agents[0].actual_phase, orange)  # 3 raz orange
    #     env = simulate_from_env(env, actions=[orange])
    #     self.assertEqual(agents[0].actual_phase, orange)  # 4 raz orange
    #     env = simulate_from_env(env, actions=[orange])
    #     self.assertEqual(agents[0].actual_phase, 1)
    #
    # def test_no_3_phase_0_action_1_orange_until_phase_1_then_back_to_0(self):
    #     agents = get_SmartAgents()
    #     actual_phase = 0
    #     orange_phase_duration = 2
    #     phase_duration = orange_phase_duration+1
    #     den = [0, 5, 10, 2]
    #     action = [1]
    #     env = single_simulate(agents, actual_phase, phase_duration, den, orange_phase_duration=orange_phase_duration,actions=action)
    #     self.assertEqual(agents[0].actual_phase, orange)
    #     simulate_from_env(env,actions=[orange])
    #     simulate_from_env(env,actions=[orange])
    #     self.assertEqual(agents[0].actual_phase, 1)
    #     simulate_from_env(env,actions=[0])
    #     simulate_from_env(env,actions=[orange])
    #     simulate_from_env(env,actions=[orange])
    #     self.assertEqual(agents[0].actual_phase, 0)
    # def test_no_4_some_batch_data(self):
    #     agents = get_SmartAgents()
    #     actual_phase = 0
    #     orange_phase_duration = 2
    #     phase_duration = orange_phase_duration + 1
    #     den = [0, 0, 10, 8]
    #     state_to_predict = LearningState(actual_phase=actual_phase, starting_actual_phase=actual_phase,
    #                                      phase_duration=phase_duration, global_densities=den + [0, 0], densities=den,
    #                                      orange_phase_duration=orange_phase_duration)
    #     for i in range(150):
    #         action = [1]
    #         # zmiana fazy - lepszy wybór
    #         env = single_simulate(agents, actual_phase, phase_duration, den, orange_phase_duration=orange_phase_duration,
    #                               actions=action)
    #         simulate_from_env(env, [orange])
    #         simulate_from_env(env, [orange])
    #         memories = env.global_memories
    #         # utrzymanie fazy - gorszy wybór
    #         action_0 = [0]
    #         env = single_simulate(agents, actual_phase, phase_duration, den, orange_phase_duration=orange_phase_duration,
    #                               actions=action_0)
    #         simulate_from_env(env, action_0)
    #         simulate_from_env(env, action_0)
    #         memories += env.global_memories
    #         save_batches(agents)
    #         batches = get_batches()
    #         train(agents=agents)
    #         prediction=agents[0].model.predict(state_to_predict.to_learn_array())
    #         # zbiega to 10,20, cokolwiek
    #         # print('prediction :)',prediction)
    #     exportData = ExportData(learningMethod='DQN', learningEpochs=0, nets=memories,
    #                             netName='net14',
    #                             densityName='test_fixed_no_4')
    #     exportData.saveToJson()
    # def test_no_5_some_batch_data(self):
    #     agents = get_SmartAgents()
    #     actual_phase = 0
    #     orange_phase_duration = 2
    #     phase_duration = orange_phase_duration + 1
    #     den = [0, 0, 10, 8]
    #     den_pred = [2, 2, 2, 78]
    #     state_to_predict = LearningState(actual_phase=actual_phase, starting_actual_phase=actual_phase,
    #                                      phase_duration=phase_duration, global_densities=den_pred + [0, 0],
    #                                      densities=den,
    #                                      orange_phase_duration=orange_phase_duration)
    #     for i in range(150):
    #         # utrzymanie fazy - gorszy wybór
    #         action_0 = [0]
    #         env = single_simulate(agents, actual_phase, phase_duration, den,
    #                               orange_phase_duration=orange_phase_duration,
    #                               actions=action_0, u=env_settings.u_all_2)
    #         for x in range(40):
    #             simulate_from_env(env, action_0)
    #             action_1 = [1]
    #         # zmiana fazy - lepszy wybór
    #         # print('stan bazowy', env.x[env.t])
    #         # print(env.global_memories[-1])
    #         simulate_from_env(env, action_1)
    #         # print('stan', env.x[env.t])
    #         # print('stan po', env.x[env.t])
    #         simulate_from_env(env, [orange])
    #         # print('stan', env.x[env.t])
    #         simulate_from_env(env, [orange])
    #         # print('stan', env.x[env.t])
    #         for x in range(20):
    #             simulate_from_env(env, action_1)
    #             # print('stan', env.x[env.t])
    #         memories = env.global_memories
    #         memories += env.global_memories
    #         save_batches(agents)
    #         batches = get_batches()
    #         train(agents=agents)
    #         env.global_memories=[]
    #         for agent in env.agents:
    #             agent.memories=[]
    #         prediction = agents[0].model.predict(state_to_predict.to_learn_array())
    #         # zbiega to 10,20, cokolwiek
    #         print('prediction :)', prediction)
    #         exportData = ExportData(learningMethod='DQN', learningEpochs=0, nets=memories,
    #                                 netName='net14',
    #                                 densityName='test_fixed_no_4')
    #         exportData.saveToJson()
    #         a=23

    def test_no_5_some_batch_data(self):
        agents = get_SmartAgents()
        actual_phase = 0
        orange_phase_duration = 2
        phase_duration = orange_phase_duration + 1
        predictions_hist = []
        # den = [0, 0, 0, 0]
        # den_pred = [2, 2, 2, 78]
        pred_x = np.array([[2, 2, 2, 78, 0]])
        # state_to_predict = LearningState(actual_phase=actual_phase, starting_actual_phase=actual_phase,
        #                                  phase_duration=phase_duration, global_densities=den_pred + [0, 0],
        #                                  densities=den,
        #                                  orange_phase_duration=orange_phase_duration)
        a=0
        for i in range(5000):
            a+=1
            # utrzymanie fazy - gorszy wybór
            action_0 = [0]
            # env = single_simulate(agents, actual_phase, phase_duration, den,
            #                       orange_phase_duration=orange_phase_duration,
            #                       actions=action_0, u=env_settings.u_all_2)
            env = Env(agents)
            for x in range(40):
                simulate_from_env(env, action_0)
            action_1 = [1]  # 41
            # zmiana fazy - lepszy wybór
            # print('stan bazowy', env.x[env.t])
            # print(env.global_memories[-1])
            if a%2==0:
                action = [1]
            else:
                action =  [0]
            simulate_from_env(env, action)  # 41
            # print('stan', env.x[env.t])
            # print('stan po', env.x[env.t])
            simulate_from_env(env, [orange])  # 42
            # print('stan', env.x[env.t])
            simulate_from_env(env, [orange])  # 43
            # print('stan', env.x[env.t])
            for x in range(20):
                simulate_from_env(env, action)
                # print('stan', env.x[env.t])
            memories = env.global_memories
            # print(f'rewardy t=40:{env.agents[0].memories[40].reward}')
            # print(f'rewardy t=41:{env.agents[0].memories[41].reward}')
            # print(f'rewardy t=42:{env.agents[0].memories[42].reward}')
            # memories += env.global_memories
            save_batches(agents)
            batches = get_batches()
            print('x batch',batches[0]['y_batch'][40])
            train(agents=agents)
            env.global_memories = []
            for agent in env.agents:
                agent.memories = []
            prediction = agents[0].model.predict(pred_x)
            predictions_hist.append(prediction)
            # zbiega to 10,20, cokolwiek
            print('prediction :)', prediction)
            exportData = ExportData(learningMethod='DQN', learningEpochs=0, nets=memories,
                                    netName='net14',
                                    densityName='test_fixed_no_4')
            # exportData.saveToJson()
            a = 23
            # plt.plot([pred[0][0] for pred in Globals().pred_plot_memory], color='red', label='0')
            # plt.plot([pred[0][1] for pred in Globals().pred_plot_memory], color='green', label='1')
            plt.plot([x[0][0] for x in predictions_hist],color='red',label='0')
            plt.plot([x[0][1] for x in predictions_hist],color='green',label='1')
            plt.legend()
            plt.title('Cokolwiek')
            plt.savefig('pred.png')
            plt.close()


if __name__ == '__main__':
    unittest.main()

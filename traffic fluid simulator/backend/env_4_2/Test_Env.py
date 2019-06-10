import random
import unittest
from typing import List

import env_data
from Env import Env, ActionInt
from env_data import max_time
from model import SmartAgent
from model.ExportData import ExportData
from nn_data import S1, S3
from services.agentFactory import get_SmartAgents
from services.globals import Globals


def get_agents_env():
    agents = get_SmartAgents()
    env = Env(agents)
    return agents, env


class Testing(unittest.TestCase):

    # def test_no_1_pass_action_1_1_1_all_time(self):
    #     # TESTUJEMY: caly czas powinna byc aktualna faza = [1,1,1]
    #     max_time = 90
    #     agents = get_SmartAgents()
    #     for agent in agents:
    #         agent.orange_phase_duration = 2
    #     Globals().time = 0
    #     env = Env(agents)
    #     env.u = env_data.u_all_2
    #     for t in range(max_time):
    #         self.assertEqual([agent.actual_phase for agent in agents], [1, 1, 1])
    #         actions = [1, 1, 1]
    #         env.step(actions)
    #     exportData = ExportData(learningMethod='Monte Carlo TODO', learningEpochs=0, nets=env.global_memories,
    #                             netName='net4',
    #                             densityName='test_no_1')
    #     exportData.saveToJson()

    def test_no_2_pass_action_1_1_1_long_time_then_2_2_2(self):
        # TESTUJEMY: zmiana faz
        max_time = 90
        agents = get_SmartAgents()
        Globals().time = 0
        env = Env(agents)
        env.u = env_data.u_all_2
        for t in range(max_time):
            # actions = [1, 1, 1] if t < 60 elif 60 == t [2, 2, 2]
            actions = [1, 1, 1]
            if t == 60 or t >= 63:
                actions = [2, 2, 2]
            if t == 61 or t == 62:
                actions = [0, 0, 0]
            # time = Globals().time # time = t
            env.step(actions)
            # time = Globals().time # time = t + 1
            if t == 60:
                self.assertEqual([agent.actual_phase for agent in agents], [1, 1, 1])
            if t == 61 or t == 62:
                self.assertEqual([agent.actual_phase for agent in agents], [0, 0, 0])
            if t >= 63:
                self.assertEqual([agent.actual_phase for agent in agents], [2, 2, 2])

        # self.assertAlmostEqual(env.x[60][20], 28.9, places=1)
        # self.assertAlmostEqual(env.x[60][5], 116, places=1)
        # self.assertEqual(env.A[60][12][5] * env.x[60][5],
        #                  10)  # wiecej niz 10 by chcialo przejechac bo 116 stoi przed swiatlami zatem A jest bardzo male
        # self.assertEqual(env.A[60][12][5], 10 / env.x[60][
        #     5])  # wiecej niz 10 by chcialo przejechac bo 116 stoi przed swiatlami zatem A jest bardzo male
        # self.assertAlmostEqual(env.x[60][12], 0.4, places=1)
        # self.assertAlmostEqual(env.x[61][12], 10, places=1)

        exportData = ExportData(learningMethod='Monte Carlo TODO', learningEpochs=0, nets=env.global_memories,
                                netName='net4',
                                densityName='test_no_2')
        exportData.saveToJson()


if __name__ == '__main__':
    unittest.main()

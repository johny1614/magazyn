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

    # def test_no_2_pass_action_1_1_1_long_time_then_2_2_2(self):
    #     # TESTUJEMY: zmiana faz
    #     max_time = 90
    #     agents = get_SmartAgents()
    #     Globals().time = 0
    #     env = Env(agents)
    #     env.u = env_data.u_all_2
    #     for t in range(max_time):
    #         # actions = [1, 1, 1] if t < 60 elif 60 == t [2, 2, 2]
    #         actions = [1, 1, 1]
    #         if t == 60 or t >= 63:
    #             actions = [2, 2, 2]
    #         if t == 61 or t == 62:
    #             actions = [0, 0, 0]
    #         # time = Globals().time # time = t
    #         env.step(actions)
    #         # time = Globals().time # time = t + 1
    #         if t == 60:
    #             self.assertEqual([agent.actual_phase for agent in agents], [1, 1, 1])
    #         if t == 61 or t == 62:
    #             self.assertEqual([agent.actual_phase for agent in agents], [0, 0, 0])
    #         if t >= 63:
    #             self.assertEqual([agent.actual_phase for agent in agents], [2, 2, 2])

    def test_no_3_pass_action_1_1_1_long_time_then_2_2_2_long_time_then_3_3_3(self):
        # TESTUJEMY: zmiana faz, phase_duration
        max_time = 90
        agents = get_SmartAgents()
        Globals().time = 0
        env = Env(agents)
        env.u = env_data.u_all_2
        for t in range(max_time):
            # actions = [1, 1, 1] if t < 60 elif 60 == t [2, 2, 2]
            actions = [1, 1, 1]
            if t == 60 or 63 <= t < 70:
                actions = [2, 2, 2]
            if t == 61 or t == 62:
                actions = [0, 0, 0]
            if t == 70 or t >= 73:
                actions = [3, 3, 3]
            if t == 71 or t == 72:
                actions = [0, 0, 0]
            # time = Globals().time # time = t
            env.step(actions)
            print(f't:{t} durations:{[agent.phase_duration for agent in env.agents]}')
            # time = Globals().time # time = t + 1
            if t == 60:
                self.assertEqual([agent.actual_phase for agent in agents], [1, 1, 1])
            if t == 61 or t == 62:
                self.assertEqual([agent.actual_phase for agent in agents], [0, 0, 0])
            if 63 >= t >= 69:
                self.assertEqual([agent.actual_phase for agent in agents], [2, 2, 2])
            if t == 70:
                self.assertEqual([agent.actual_phase for agent in agents], [2, 2, 2])
            if t == 71 or t == 72:
                self.assertEqual([agent.actual_phase for agent in agents], [0, 0, 0])
            if t >= 73:
                self.assertEqual([agent.actual_phase for agent in agents], [3, 3, 3])


            # phase_duration Testujemy
            if t == 60:
                self.assertEqual([agent.phase_duration for agent in agents], [0,0,0])
            if t == 61:
                self.assertEqual([agent.phase_duration for agent in agents], [0,0,0])
            if t == 62:
                self.assertEqual([agent.phase_duration for agent in agents], [1,1,1])
            if t == 63:
                self.assertEqual([agent.phase_duration for agent in agents], [2,2,2])

            if t == 70:
                self.assertEqual([agent.phase_duration for agent in agents], [0,0,0])
            if t == 71:
                self.assertEqual([agent.phase_duration for agent in agents], [0,0,0])
            if t == 72:
                self.assertEqual([agent.phase_duration for agent in agents], [1,1,1])
            if t == 73:
                self.assertEqual([agent.phase_duration for agent in agents], [2,2,2])


        exportData = ExportData(learningMethod='Monte Carlo TODO', learningEpochs=0, nets=env.global_memories,
                                netName='net4',
                                densityName='test_no_3')
        exportData.saveToJson()
        print('oK')


if __name__ == '__main__':
    unittest.main()
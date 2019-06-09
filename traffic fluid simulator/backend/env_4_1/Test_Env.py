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

    def test_no_1_pass_action_1_1_1_all_time(self):
        # u - wplywaja co chwile 2 pojazdy wszedzie
        # caly czasz dajemy akcje [1,1,1]
        # Przechodza wszystkie pojazdy w time stepie
        # orange_phase_duration = 0 tak samo jak phase_duration
        # TESTUJEMY: rewardy
        max_time = 90
        agents = get_SmartAgents()
        for agent in agents:
            agent.orange_phase_duration = 0
        Globals().time = 0
        env = Env(agents)
        env.u = env_data.u_all_2
        for t in range(max_time):
            actions = [1, 1, 1]
            env.step(actions)
            # print(f't:{t} {env.global_rewards[t]}')
            if 0 <= t <= 2:
                self.assertEqual(env.global_rewards[t], [0, 0, 0])  # nic nie przeplywa jeszcze w ogole
            if 3 <= t <= 11:
                self.assertEqual(env.global_rewards[t][0], 2)  # jedynie agent 0 ma przeplyw 2
        exportData = ExportData(learningMethod='Monte Carlo TODO', learningEpochs=0, nets=env.global_memories,
                                netName='net4',
                                densityName='test_no_1')
        exportData.saveToJson()

    def test_no_2_pass_action_1_1_1_long_time_then_2_2_2(self):
        # u - wplywaja co chwile 2 pojazdy wszedzie
        # caly czasz dajemy akcje [1,1,1]
        # Przechodza wszystkie pojazdy w time stepie
        # orange_phase_duration = 0 tak samo jak phase_duration
        # TESTUJEMY: rewardy, zmiana faz, zmiana A
        max_time = 90
        agents = get_SmartAgents()
        for agent in agents:
            agent.orange_phase_duration = 0
        Globals().time = 0
        env = Env(agents)
        env.u = env_data.u_all_2
        for i in range(max_time):
            t=Globals().time
            actions = [1, 1, 1] if t < 60 else [2, 2, 2]
            env.step(actions)
            if t < 60:
                self.assertEqual([agent.actual_phase for agent in agents],[1,1,1])
            if t>=60:
                self.assertEqual([agent.actual_phase for agent in agents],[2,2,2])
            print(f't:{t} {env.global_rewards[t]}')
        self.assertTrue(env.global_rewards[60][0] > 30)  # 30.28 to reward
        self.assertTrue(env.global_rewards[60][1] > 110)  # 116.8 to reward
        self.assertTrue(env.global_rewards[60][2] > 110)  # 116.8 to reward

        self.assertEqual(env.A[59][27][17], 0.7)  # w chwili 59 do sekcji 27 przejezda z sekcji 17 dokladnie 0.7
        self.assertEqual(env.A[60][27][17], 0.0)    # w chwili 60 do sekcji 27 przejezda z sekcji 17 dokladnie 0

        self.assertEqual(env.A[59][15][8], 0)    # w chwili 59 do sekcji 15 przejezda z sekcji 8 dokladnie 0
        self.assertEqual(env.A[60][15][8], 0.7)  # w chwili 60 do sekcji 15 przejezda z sekcji 8 dokladnie 0.7



        exportData = ExportData(learningMethod='Monte Carlo TODO', learningEpochs=0, nets=env.global_memories,
                                netName='net4',
                                densityName='test_no_2')
        exportData.saveToJson()


if __name__ == '__main__':
    unittest.main()

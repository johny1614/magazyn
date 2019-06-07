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
        max_time = 90
        agents = get_SmartAgents()
        for agent in agents:
            agent.orange_phase_duration=0
        env = Env(agents)
        env.u = env_data.u_all_2
        Globals().time = 0
        for t in range(max_time):
            actions = [1, 1, 1]
            env.step(actions)
            print(f't:{t} {env.global_rewards[t]}')
        # self.assertEqual(env.A[(27, 20)], 0.3)
        exportData = ExportData(learningMethod='Monte Carlo TODO', learningEpochs=0, nets=env.global_memories, netName='net4',
                                densityName='test_no_1')
        exportData.saveToJson()


if __name__ == '__main__':
    unittest.main()

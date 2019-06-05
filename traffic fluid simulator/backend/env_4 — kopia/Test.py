import random
import unittest
from typing import List

from Env import Env, ActionInt
from env_data import max_time
from model import SmartAgent
from nn_data import S1, S3
from services.agentFactory import get_SmartAgents
from services.globals import Globals


def get_agents_env():
    agents = get_SmartAgents()
    env = Env(agents)
    return agents, env


class Testing(unittest.TestCase):

    def test_pass_action_1_1_1_all_time(self):
        # actions: 2, wait, wait and we have 2 phase on
        max_time = 90
        agents = get_SmartAgents()
        Globals().time = 0
        env = Env(agents)
        for t in range(max_time):
            actions = [1, 1, 1]
            env.step(actions)
            if t > 5:
                self.assertEqual(env.A[(9, 2)], 0.7)

    def test_pass_action_1_1_1_long_time_then_2_1_2(self):
        # actions: 2, wait, wait and we have 2 phase on
        max_time = 90
        agents = get_SmartAgents()
        Globals().time = 0
        env = Env(agents)
        for t in range(max_time):
            actions = [1, 1, 1]
            if t > 50:
                actions = [2, 1, 2]
            env.step(actions)
            if t > 56:
                self.assertEqual(env.A[(27,20)],0.3)



if __name__ == '__main__':
    unittest.main()

import random
import unittest
from typing import List

import numpy as np

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
    def test_learn_no_1_pass_action_1_1_1_long_time_then_2_2_2(self):
        # u - wplywaja co chwile 2 pojazdy wszedzie
        # caly czas dajemy akcje [1,1,1]
        # w momencie 60 dajemy akcje [2,2,2]
        # Przechodza wszystkie pojazdy w time stepie
        # orange_phase_duration = 0 tak samo jak phase_duration
        # TESTUJEMY: czy SmartAgenci sie ucza na podstawie poprawnych nagrod i stanow
        max_time = 90
        agents = get_SmartAgents()
        for agent in agents:
            agent.orange_phase_duration = 0
        Globals().time = 0
        env = Env(agents)
        env.u = env_data.u_all_2
        for t in range(max_time):
            actions = [1, 1, 1] if t < 60 else [2, 2, 2]
            env.step(actions)
            if t < 60:
                self.assertEqual([agent.actual_phase for agent in agents], [1, 1, 1])
            if t >= 60:
                self.assertEqual([agent.actual_phase for agent in agents], [2, 2, 2])
        self.assertEqual(agents[0].memories[60].action, 2)
        self.assertAlmostEqual(agents[0].memories[60].reward, 20.0, 0)

        # Moment 60
        real_state = agents[0].memories[60].state.to_learn_nd_array()
        expected_state = np.array([[1, 4, 1]])  # densities are 2.0,28.88,0.18 so groups are 1,5,1
        np.testing.assert_almost_equal(real_state, expected_state, decimal=0)

        # Moment 61
        real_state = agents[0].memories[61].state.to_learn_nd_array()
        expected_state = np.array([[1, 3, 1]])  # densities are 2.6,10.8,0.3 so groups are 1,5,1
        np.testing.assert_almost_equal(real_state, expected_state, decimal=0)

        Globals().batch_size = 90
        for agent in env.agents:
            agent.train()

        exportData = ExportData(learningMethod='Monte Carlo TODO', learningEpochs=0, nets=env.global_memories,
                                netName='net4',
                                densityName='test_learn_no_2')
        exportData.saveToJson()
        # if 0 <= t <= 2:
        #     self.assertEqual(env.global_rewards[t],[0,0,0]) # nic nie przeplywa jeszcze w ogole
        # if 3 <= t <= 11:
        #     self.assertEqual(env.global_rewards[t][0],2) # jedynie agent 0 ma przeplyw 2


if __name__ == '__main__':
    unittest.main()

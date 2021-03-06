import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))
import unittest
import env_settings
from Env import Env
from model.ExportData import ExportData
from services.agentFactory import get_SmartAgents
from services.globals import Globals

yellow = 'yellow'


class Testing(unittest.TestCase):
    def test_no_0_pass_action_0_all_time(self):
        max_time = 90
        agents = get_SmartAgents()
        Globals().time = 0
        env = Env(agents)
        env.u = env_settings.u_all_2
        for t in range(max_time):
            if t >= 3:
                self.assertEqual([agent.actual_phase for agent in agents], [0])
            actions = [0]
            env.step(actions)
        exportData = ExportData(learningMethod='None', learningEpochs=0, nets=env.global_memories,
                                netName='net11',
                                densityName='test_no_0')
        exportData.saveToJson()

    def test_no_2_pass_action_0_then_1_then_0(self):
        max_time = 90
        agents = get_SmartAgents()
        Globals().time = 0
        env = Env(agents)
        env.u = env_settings.u_all_2
        for t in range(max_time):
            if t < 20:
                actions = [0]
            elif t < 40:
                actions = [1]
            else:
                actions = [0]
            env.step(actions)
            if t < 20:
                self.assertEqual(agents[0].actual_phase, 0)
            elif t < 40:
                self.assertEqual(agents[0].actual_phase, 1)
            else:
                self.assertEqual(agents[0].actual_phase, 0)
        exportData = ExportData(learningMethod='None', learningEpochs=0, nets=env.global_memories,
                                netName='net11',
                                densityName='test_no_2')
        exportData.saveToJson()


if __name__ == '__main__':
    unittest.main()

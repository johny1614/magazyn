import os
import sys
sys.path.append(os.path.dirname(os.getcwd()))
from model.Action import yellow
import env_settings
from model.ExportData import ExportData
from services.globals import Globals
import unittest
from Env import Env
from services.agentFactory import get_SmartAgents


yellow = 'yellow'


class Testing(unittest.TestCase):
    def test_no_1_pass_action_0_all_time(self):
        # TESTUJEMY: caly czas powinna byc aktualna faza = [0]
        max_time = 90
        agents = get_SmartAgents()
        for agent in agents:
            agent.yellow_phase_duration = 2
        Globals().time = 0
        env = Env(agents)
        env.u = env_settings.u_all_2
        for t in range(max_time):
            if t >= 3:
                self.assertEqual([agent.actual_phase for agent in agents], [0])
            actions = [0]
            env.step(actions)
        exportData = ExportData(learningMethod='Monte Carlo TODO', learningEpochs=0, nets=env.global_memories,
                                netName='net14',
                                densityName='test_no_1')
        exportData.saveToJson()


    def test_no_2_pass_action_0_long_time_then_1(self):
        # TESTUJEMY: zmiana faz
        max_time = 90
        agents = get_SmartAgents()
        for agent in agents:
            agent.yellow_phase_duration = 2
        Globals().time = 0
        env = Env(agents)
        env.u = env_settings.u_all_2
        env.yellow_phase_duration = 2
        for t in range(max_time):
            actions = [0]
            if t == 60 or t > 62:
                actions = [1]
            if t == 61 or t == 62:
                actions = [yellow]
            time = Globals().time # time = t
            env.step(actions)
            time = Globals().time # time = t + 1
            if t in range(3, 60):
                self.assertEqual([agent.actual_phase for agent in agents], [0])
            if t == 60 or t == 61:
                self.assertEqual([agent.actual_phase for agent in agents], [yellow])
            if t >= 62:
                self.assertEqual([agent.actual_phase for agent in agents], [1])
            exportData = ExportData(learningMethod='Nothing', learningEpochs=0, nets=env.global_memories,
                                    netName='net14',
                                    densityName='test_no_2')
            exportData.saveToJson()


    def test_no_3_pass_action_0_then_1_then_0(self):
        # TESTUJEMY: zmiana faz, phase_duration
        max_time = 90
        agents = get_SmartAgents()
        for agent in agents:
            agent.yellow_phase_duration = 2
        Globals().time = 0
        env = Env(agents)
        env.u = env_settings.u_all_2
        env.yellow_phase_duration = 2
        for t in range(max_time):
            # actions = [1] if t < 60 elif 60 == t [2]
            actions = [0, 0, 0]
            if t == 60 or 63 <= t < 70:
                actions = [1]
            if t == 61 or t == 62:
                actions = [yellow]
            if t == 70 or t >= 73:
                actions = [0]
            if t == 71 or t == 72:
                actions = [yellow]
            env.step(actions)
            if t == 60 or t == 61:
                self.assertEqual([agent.actual_phase for agent in agents], [yellow])
            if 63 >= t >= 69:
                self.assertEqual([agent.actual_phase for agent in agents], [1])
            if t == 70 or t == 71:
                self.assertEqual([agent.actual_phase for agent in agents], [yellow])
            if t >= 73:
                self.assertEqual([agent.actual_phase for agent in agents], [0])
            #
            #
            # phase_duration Testujemy
            if t == 60:
                self.assertEqual([agent.phase_duration for agent in agents], [0])
            if t == 61:
                self.assertEqual([agent.phase_duration for agent in agents], [1])
            if t == 62:
                self.assertEqual([agent.phase_duration for agent in agents], [2])  # faza 0 trwa juz 2, przelaczylismy wlasnie na faze 0, ale nie musimy zerowac phase_duration
            if t == 63:
                self.assertEqual([agent.phase_duration for agent in agents], [3])  # w chwili
            if t == 70:
                self.assertEqual([agent.phase_duration for agent in agents], [0])
            if t == 71:
                self.assertEqual([agent.phase_duration for agent in agents], [1])
            if t == 72:
                self.assertEqual([agent.phase_duration for agent in agents], [2])
            if t == 73:
                self.assertEqual([agent.phase_duration for agent in agents], [3])

        exportData = ExportData(learningMethod='Monte Carlo TODO', learningEpochs=0, nets=env.global_memories,
                                netName='net14',
                                densityName='test_no_3')
        exportData.saveToJson()


    def test_no_4_pass_action_0_1_0(self):
        # TESTUJEMY: actual_phase - czy jest ono zgodne rowniez w memories
        max_time = 90
        agents = get_SmartAgents()
        for agent in agents:
            agent.yellow_phase_duration = 2
        Globals().time = 0
        env = Env(agents)
        env.u = env_settings.u_all_2
        env.yellow_phase_duration = 2
        for t in range(max_time):
            # actions = [0, 0, 0] if t < 60 elif 60 == t [1, 1, 1]
            actions = [0]
            if t == 60 or 63 <= t < 70:
                actions = [1]
            if t == 61 or t == 62:
                actions = [yellow]
            if t == 70 or t >= 73:
                actions = [0]
            if t == 71 or t == 72:
                actions = [yellow]
            env.step(actions)
            # print(f't:{t}, {agents[0].actual_phase}')
            if t in range(3, 60):
                self.assertEqual([agent.actual_phase for agent in agents],
                                 [0])  # Po operacji w chwili 60 mamy taka faze dla stanu w chwili 60
                self.assertEqual([agent.memories[t].state.actual_phase for agent in agents],
                                 [0])  # Po operacji w chwili 60 mamy taka faze dla stanu w chwili 60
            if t == 60 or t == 61:
                self.assertEqual([agent.actual_phase for agent in agents], [yellow])
                self.assertEqual([agent.memories[t].state.actual_phase for agent in agents], [yellow])
            if 62 <= t <= 69:
                self.assertEqual([agent.actual_phase for agent in agents], [1])
                self.assertEqual([agent.memories[t].state.actual_phase for agent in agents], [1])
            if t == 70 or t == 71:
                self.assertEqual([agent.actual_phase for agent in agents], [yellow])
                self.assertEqual([agent.memories[t].state.actual_phase for agent in agents], [yellow])
            if t >= 72:
                self.assertEqual([agent.actual_phase for agent in agents], [0])
                self.assertEqual([agent.memories[t].state.actual_phase for agent in agents], [0])

        exportData = ExportData(learningMethod='Monte Carlo TODO', learningEpochs=0, nets=env.global_memories,
                                netName='net14',
                                densityName='test_no_4')
        exportData.saveToJson()


if __name__ == '__main__':
    unittest.main()

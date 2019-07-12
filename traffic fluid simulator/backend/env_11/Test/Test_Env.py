import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))
import unittest
from typing import List
import env_settings
from Env import Env
from model import SmartAgent
from model.ExportData import ExportData
from services.agentFactory import get_SmartAgents
from services.globals import Globals


def get_agents_env():
    agents = get_SmartAgents()
    env = Env(agents)
    return agents, env


orange = 'orange'


class Testing(unittest.TestCase):
    def test_no_1_pass_action_0_all_time(self):
        # TESTUJEMY: caly czas powinna byc aktualna faza = [0]
        max_time = 90
        agents = get_SmartAgents()
        for agent in agents:
            agent.orange_phase_duration = 2
        Globals().time = 0
        env = Env(agents)
        env.u = env_settings.u_all_2
        for t in range(max_time):
            if t >= 3:
                self.assertEqual([agent.actual_phase for agent in agents], [0])
            actions = [0]
            env.step(actions)
        exportData = ExportData(learningMethod='Monte Carlo TODO', learningEpochs=0, nets=env.global_memories,
                                netName='net11',
                                densityName='test_no_1')
        exportData.saveToJson()

    def test_no_2_pass_action_0_long_time_then_1(self):
        # TESTUJEMY: zmiana faz
        max_time = 90
        agents = get_SmartAgents()
        Globals().time = 0
        env = Env(agents)
        env.u = env_settings.u_all_2
        for t in range(max_time):
            # actions = [1, 1, 1] if t < 60 elif 60 == t [2, 2, 2]
            actions = [0]
            if t == 60 or t > 62:
                actions = [1]
            if t == 61 or t == 62:
                actions = ['orange']
            # time = Globals().time # time = t
            env.step(actions)
            # time = Globals().time # time = t + 1
            if t in range(3, 60):
                self.assertEqual([agent.actual_phase for agent in agents], [0])
            if t == 60 or t == 61:
                self.assertEqual([agent.actual_phase for agent in agents], ['orange'])
            if t >= 62:
                self.assertEqual([agent.actual_phase for agent in agents], [1])

    def test_no_3_pass_action_0_then_1_then_0(self):
        # TESTUJEMY: zmiana faz, phase_duration
        max_time = 90
        agents = get_SmartAgents()
        Globals().time = 0
        env = Env(agents)
        env.u = env_settings.u_all_2
        orange = 'orange'
        for t in range(max_time):
            # actions = [1] if t < 60 elif 60 == t [2]
            actions = [0, 0, 0]
            if t == 60 or 63 <= t < 70:
                actions = [1]
            if t == 61 or t == 62:
                actions = [orange]
            if t == 70 or t >= 73:
                actions = [0]
            if t == 71 or t == 72:
                actions = [orange]
            env.step(actions)
            if t == 60 or t == 61:
                self.assertEqual([agent.actual_phase for agent in agents], [orange])
            if 63 >= t >= 69:
                self.assertEqual([agent.actual_phase for agent in agents], [1])
            if t == 70 or t == 71:
                self.assertEqual([agent.actual_phase for agent in agents], [orange])
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
                                netName='net11',
                                densityName='test_no_3')
        exportData.saveToJson()
    #
    def test_no_4_pass_action_0_1_0(self):
        # TESTUJEMY: actual_phase - czy jest ono zgodne rowniez w memories
        max_time = 90
        agents = get_SmartAgents()
        Globals().time = 0
        env = Env(agents)
        env.u = env_settings.u_all_2
        for t in range(max_time):
            # actions = [0, 0, 0] if t < 60 elif 60 == t [1, 1, 1]
            actions = [0]
            if t == 60 or 63 <= t < 70:
                actions = [1]
            if t == 61 or t == 62:
                actions = [orange]
            if t == 70 or t >= 73:
                actions = [0]
            if t == 71 or t == 72:
                actions = [orange]
            env.step(actions)
            # print(f't:{t}, {agents[0].actual_phase}')
            if t in range(3, 60):
                self.assertEqual([agent.actual_phase for agent in agents],
                                 [0])  # Po operacji w chwili 60 mamy taka faze dla stanu w chwili 60
                self.assertEqual([agent.memories[t].state.actual_phase for agent in agents],
                                 [0])  # Po operacji w chwili 60 mamy taka faze dla stanu w chwili 60
            if t == 60 or t == 61:
                self.assertEqual([agent.actual_phase for agent in agents], [orange])
                self.assertEqual([agent.memories[t].state.actual_phase for agent in agents], [orange])
            if 62 <= t <= 69:
                self.assertEqual([agent.actual_phase for agent in agents], [1])
                self.assertEqual([agent.memories[t].state.actual_phase for agent in agents], [1])
            if t == 70 or t == 71:
                self.assertEqual([agent.actual_phase for agent in agents], [orange])
                self.assertEqual([agent.memories[t].state.actual_phase for agent in agents], [orange])
            if t >= 72:
                self.assertEqual([agent.actual_phase for agent in agents], [0])
                self.assertEqual([agent.memories[t].state.actual_phase for agent in agents], [0])

        exportData = ExportData(learningMethod='Monte Carlo TODO', learningEpochs=0, nets=env.global_memories,
                                netName='net11',
                                densityName='test_no_4')
        exportData.saveToJson()

    def test_no_5_reshaping_pass_action_0_1_0(self):
        # TESTUJEMY - starting_actual_phase
        max_time = 90
        agents = get_SmartAgents()
        Globals().time = 0
        Globals().gamma = 0
        env = Env(agents)
        env.u = env_settings.u_all_2
        for t in range(max_time):
            actions = [0]
            if t == 60 or 63 <= t < 70:
                actions = [1]
            if t == 61 or t == 62:
                actions = [orange]
            if t == 70 or t >= 73:
                actions = [0]
            if t == 71 or t == 72:
                actions = [orange]
            env.step(actions)
            # print(f't:{t}, actual_phase:{agents[0].actual_phase}')
            if 3 <= t < 60:
                self.assertEquals([agent.starting_actual_phase for agent in agents], [0])
                self.assertEquals([agent.actual_phase for agent in agents], [0])
            if t == 60:
                self.assertEquals([agent.starting_actual_phase for agent in agents], [0])
                self.assertEquals([agent.actual_phase for agent in agents], [orange])
            if t == 61:
                self.assertEquals([agent.starting_actual_phase for agent in agents], [orange])
                self.assertEquals([agent.actual_phase for agent in agents], [orange])
            if t == 62:
                self.assertEquals([agent.starting_actual_phase for agent in agents], [orange])
                self.assertEquals([agent.actual_phase for agent in agents], [1])
            if 63 <= t <= 69:
                self.assertEquals([agent.starting_actual_phase for agent in agents], [1])
                self.assertEquals([agent.actual_phase for agent in agents], [1])
            if t == 70:
                self.assertEquals([agent.starting_actual_phase for agent in agents], [1])
                self.assertEquals([agent.actual_phase for agent in agents], [orange])
            if t == 71:
                self.assertEquals([agent.starting_actual_phase for agent in agents], [orange])
                self.assertEquals([agent.actual_phase for agent in agents], [orange, ])
            if t == 72:
                self.assertEquals([agent.starting_actual_phase for agent in agents], [orange, ])
                self.assertEquals([agent.actual_phase for agent in agents], [0])

    def test_no_5_reshaping_pass_action_0_1_0(self):
        # TESTUJEMY: rewardy
        max_time = 90
        agents = get_SmartAgents()
        Globals().time = 0
        Globals().gamma = 0
        env = Env(agents)
        env.u = env_settings.u_all_2
        for t in range(max_time):
            # actions = [0,0,0] if t < 60 elif 60 == t [1,1,1]
            actions = [0]
            if t == 1 or t == 2:
                actions = [orange]
            if t == 60 or 63 <= t < 70:
                actions = [1]
            if t == 61 or t == 62:
                actions = [orange]
            if t == 70 or t >= 73:
                actions = [0]
            if t == 71 or t == 72:
                actions = [orange]
            env.step(actions)
        env.agents[0].save_batch()
        env.agents[0].reshape_rewards()
        self.assertAlmostEqual(env.agents[0].memories[60].reward, 2, 0)
        self.assertAlmostEqual(env.agents[0].memories[61].reward, 4, 0)
        self.assertAlmostEqual(env.agents[0].memories[62].reward, 6, 0)
        # env.update_memory_rewards()
        exportData = ExportData(learningMethod='Monte Carlo TODO', learningEpochs=0, nets=env.global_memories,
                                netName='net11', densityName='test_no_6')
        exportData.saveToJson()

    def test_no_5_reshaping_pass_action_0_1_0(self):
        # TESTUJEMY: rewardy
        max_time = 90
        agents = get_SmartAgents()
        Globals().time = 0
        Globals().gamma = 0
        env = Env(agents)
        env.u = env_settings.u_all_9
        for t in range(max_time):
            # actions = [0,0,0] if t < 60 elif 60 == t [1,1,1]
            actions = [0]
            if t == 1 or t == 2:
                actions = [orange]
            if t == 60 or 63 <= t < 70:
                actions = [1]
            if t == 61 or t == 62:
                actions = [orange]
            if t == 70 or t >= 73:
                actions = [0]
            if t == 71 or t == 72:
                actions = [orange]
            env.step(actions)
        env.agents[0].save_batch()
        env.agents[0].reshape_rewards()
        # self.assertAlmostEqual(env.agents[0].memories[60].reward, 2, 0)
        # self.assertAlmostEqual(env.agents[0].memories[61].reward, 4, 0)
        # self.assertAlmostEqual(env.agents[0].memories[62].reward, 6, 0)
        # env.update_memory_rewards()
        exportData = ExportData(learningMethod='Monte Carlo TODO', learningEpochs=0, nets=env.global_memories,
                                netName='net11', densityName='test_no_6')
        exportData.saveToJson()

    #
    # #
    # def test_no_6_starting_phase_actual_phase(self):
    #     # Testujemy stargin_actual_phase - jest potrzebne do learningState
    #     agents: List[SmartAgent] = get_SmartAgents()
    #     # for agent in agents:
    #     #     agent.model = agent._build_model(layers=[20, 50, 30, 18])
    #     env = Env(agents)
    #     env.u = env_settings.u_all_2
    #     max_time = 90
    #     Globals().time = 0
    #     for t in range(max_time):
    #         # actions = [0, 0, 0] if t < 60 elif 60 == t [1, 1, 1]
    #         actions = [0, 0, 0]
    #         if t == 1 or t == 2:
    #             actions = [orange, orange, orange]
    #         if t == 60 or t >= 63:
    #             actions = [1, 1, 1]
    #         if t == 61 or t == 62 or t == 71 or t == 72:
    #             actions = [orange, orange, orange]
    #         if t == 70 or t >= 72:
    #             actions = [2, 2, 2]
    #         env.step(actions)
    #     for agent in agents:
    #         agent.reshape_rewards()
    #     self.assertEqual(agents[0].memories[60].state.starting_actual_phase, 0)
    #     self.assertEqual(agents[0].memories[61].state.starting_actual_phase, orange)
    #     self.assertEqual(agents[0].memories[62].state.starting_actual_phase, orange)
    #     self.assertEqual(agents[0].memories[63].state.starting_actual_phase, 1)
    #
    #     self.assertEqual(agents[0].memories[70].state.starting_actual_phase, 1)
    #     self.assertEqual(agents[0].memories[71].state.starting_actual_phase, orange)
    #     self.assertEqual(agents[0].memories[72].state.starting_actual_phase, orange)
    #     self.assertEqual(agents[0].memories[73].state.starting_actual_phase, 2)
    #
    #     exportData = ExportData(learningMethod='Monte Carlo TODO', learningEpochs=0, nets=env.global_memories,
    #                             netName='net11',
    #                             densityName='test_learn_no_1')
    #     exportData.saveToJson()


if __name__ == '__main__':
    unittest.main()

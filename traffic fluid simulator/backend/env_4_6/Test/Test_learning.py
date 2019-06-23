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


class Testing(unittest.TestCase):
    def test_no_1_111_then_222_what_is_brilliant_idea(self):
        agents: List[SmartAgent] = get_SmartAgents()
        for agent in agents:
            agent.model = agent._build_model(layers=[20, 50, 30, 18])
        env = Env(agents)
        env.u = env_settings.u_all_2
        max_time = 90
        Globals().time = 0
        for t in range(max_time):
            # actions = [1, 1, 1] if t < 60 elif 60 == t [2, 2, 2]
            actions = [1, 1, 1]
            if t == 60 or t >= 62:
                actions = [2, 2, 2]
            if t == 61:
                actions = [0, 0, 0]
            env.step(actions)
        for agent in agents:
            agent.reshape_rewards()
        exportData = ExportData(learningMethod='DQN', learningEpochs=0, nets=env.global_memories,
                                netName='net4',
                                densityName='test_learn_no_1')
        exportData.saveToJson()
        agents[0].train_full(epochs=7000,learning_rate=0.001)
        x=[2,2,2]+[0.6,0.6,28.88]+[0.126,0.126,0.18]+[1]

if __name__ == '__main__':
    unittest.main()

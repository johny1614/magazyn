import random
import unittest

from Env import Env
from model import SmartAgent
from nn_data import S1, S3
from services.agentFactory import get_SmartAgents


def get_agents_env():
    agents = get_SmartAgents()
    env = Env(agents)
    return agents, env


class Testing(unittest.TestCase):

    # def test_initial_action_space_all_3_phases(self):
    #     agents, env = get_agents_env()
    #     agent = env.agents[0]
    #     # agent.local_action_space[0]
    #     self.assertEqual(len(agent.local_action_space), 3)
    #
    # def test_pass_action_2(self):
    #     agents, env = get_agents_env()
    #     agent = env.agents[0]
    #     agent.orange_phase_duration = 0
    #     action_2 = [action for action in agent.local_action_space if action.index == 2][0]
    #     agent.pass_action(action_2)  # D
    #     print('----')
    #     self.assertEqual(agent.actual_phase, action_2.decided_phase)
    #
    # def test_pass_action_2_several_times_no_orange_duration(self):
    #     print('test_pass_action_2_several_times_no_orange_duration ---------')
    #     agents, env = get_agents_env()
    #     agent = env.agents[0]
    #     agent.orange_phase_duration = 0
    #     action_2 = [action for action in agent.local_action_space if action.index == 2][0]
    #     agent.pass_action(action_2)  # D
    #     agent.pass_action(action_2)  # C
    #     agent.pass_action(action_2)  # C
    #     print('----')
    #     self.assertEqual(agent.actual_phase, action_2.decided_phase)
    #
    # def test_pass_action_2_several_times_then_3_no_orange_duration(self):
    #     print('test_pass_action_2_several_times_then_3_no_orange_duration ------')
    #     agents, env = get_agents_env()
    #     agent = env.agents[0]
    #     agent.orange_phase_duration = 0
    #     action_2 = [action for action in agent.local_action_space if action.index == 2][0]
    #     agent.pass_action(action_2)  # D
    #     agent.pass_action(action_2)  # C
    #     agent.pass_action(action_2)  # C
    #     self.assertEqual(agent.actual_phase, action_2.decided_phase)
    #     action_3 = [action for action in agent.local_action_space if action.index == 3][0]
    #     agent.pass_action(action_3)  # D
    #     self.assertEqual(agent.actual_phase, action_3.decided_phase)

    def test_pass_action_2_several_times(self):
        # actions: 2, wait, wait and we have 2 phase on
        agents, env = get_agents_env()
        agent = env.agents[0]
        agent.orange_phase_duration = 2
        action_2 = [action for action in agent.local_action_space if action.index == 2][0]
        agent.pass_action(action_2)
        wait_action=agent.local_action_space[0]
        agent.pass_action(wait_action)
        agent.pass_action(wait_action)
        self.assertEqual(agent.actual_phase, agent.all_phases[2])

    # def test_pass_actual_phase_action(self):
    #     env = self.get_env()
    #     agent = env.agents[0]
    #     action = 2
    #     agent.pass_action(action)
    #     for i in range(agent.orange_phase_duration - 1):
    #         agent.pass_action('wait')
    #     agent.pass_action('wait')
    #     self.assertEqual(agent.actual_phase, agent.all_phases[2])
    #     # here we have action number 2 atm
    #     agent.pass_action(2)
    #     self.assertEqual(agent.actual_phase,agent.all_phases[2])
    #
    # def test_pass_new_phase_action(self):
    #     env = self.get_env()
    #     agent = env.agents[0]
    #     action = 2
    #     agent.pass_action(action)
    #     for i in range(agent.orange_phase_duration - 1):
    #         agent.pass_action('wait')
    #     agent.pass_action('wait')
    #     self.assertEqual(agent.actual_phase, agent.all_phases[2])
    #     # here we have action number 2 atm
    #     agent.pass_action(1)
    #     # here we have for a while orange
    #     for i in range(agent.orange_phase_duration-1):
    #         agent.pass_action('wait')
    #         self.assertEqual(agent.actual_phase,agent.all_phases[0])
    #     agent.pass_action('wait')
    #     # now we should have our 1 action
    #     self.assertEqual(agent.actual_phase,agent.all_phases[1])
    # def test_pass_all_3_actions(self):
    #     max_time=30
    #     env = self.get_env()
    #     for time in range(max_time - 1):
    #         global_action_space = env.get_global_action_space()
    #         actions = [random.choice(local_action_space) for local_action_space in global_action_space]
    #         if (actions[0] == 'wait'):
    #             actions = ['wait'] * 3
    #         elif (time < 14):
    #             actions = [1, 1, 1]
    #         elif (time >= 20 and actions[0] != 'wait'):
    #             actions = [3, 3, 3]
    #         elif (time >= 14 and actions[0] != 'wait'):
    #             actions = [2, 2, 2]
    #         # if(time>1 and time<14):
    #         #     self.assertEqual(env.A[][])

    def test_pass_action_2_several_times(self):
        # actions: 2, wait, wait and we have 2 phase on
        agents, env = get_agents_env()
        agent:SmartAgent = env.agents[0]
        for state in S3:
            agent.states_map.add_state(state)
        agent.states_map.update_clusters()
        cluster_2 = agent.states_map.get_cluster(S3[2])
        cluster_3 = agent.states_map.get_cluster(S3[3])
        cluster_last = agent.states_map.get_cluster(S3[-1])
        print(cluster_2)
        print(cluster_3)
        print(cluster_last)
        print(cluster_2.index)
        print(cluster_3.index)
        print(cluster_last.index)

if __name__ == '__main__':
    unittest.main()

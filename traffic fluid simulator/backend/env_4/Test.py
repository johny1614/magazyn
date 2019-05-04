import random
import unittest

from Env import Env


class Testing(unittest.TestCase):

    def get_env(self):
        return Env()

    def test_pass_initial_action(self):
        env = self.get_env()
        agent=env.agents[0]
        action=2
        agent.pass_action(action)
        for i in range(agent.orange_phase_duration-1):
            agent.pass_action('wait')
            self.assertEqual(agent.actual_phase,agent.all_phases[0])
        agent.pass_action('wait')
        self.assertEqual(agent.actual_phase, agent.all_phases[2])

    def test_pass_actual_phase_action(self):
        env = self.get_env()
        agent = env.agents[0]
        action = 2
        agent.pass_action(action)
        for i in range(agent.orange_phase_duration - 1):
            agent.pass_action('wait')
        agent.pass_action('wait')
        self.assertEqual(agent.actual_phase, agent.all_phases[2])
        # here we have action number 2 atm
        agent.pass_action(2)
        self.assertEqual(agent.actual_phase,agent.all_phases[2])

    def test_pass_new_phase_action(self):
        env = self.get_env()
        agent = env.agents[0]
        action = 2
        agent.pass_action(action)
        for i in range(agent.orange_phase_duration - 1):
            agent.pass_action('wait')
        agent.pass_action('wait')
        self.assertEqual(agent.actual_phase, agent.all_phases[2])
        # here we have action number 2 atm
        agent.pass_action(1)
        # here we have for a while orange
        for i in range(agent.orange_phase_duration-1):
            agent.pass_action('wait')
            self.assertEqual(agent.actual_phase,agent.all_phases[0])
        agent.pass_action('wait')
        # now we should have our 1 action
        self.assertEqual(agent.actual_phase,agent.all_phases[1])
    def test_pass_all_3_actions(self):
        max_time=30
        env = self.get_env()
        for time in range(max_time - 1):
            global_action_space = env.get_global_action_space()
            actions = [random.choice(local_action_space) for local_action_space in global_action_space]
            if (actions[0] == 'wait'):
                actions = ['wait'] * 3
            elif (time < 14):
                actions = [1, 1, 1]
            elif (time >= 20 and actions[0] != 'wait'):
                actions = [3, 3, 3]
            elif (time >= 14 and actions[0] != 'wait'):
                actions = [2, 2, 2]
            # if(time>1 and time<14):
            #     self.assertEqual(env.A[][])

if __name__ == '__main__':
    unittest.main()

import unittest

from env import Env


class Testing(unittest.TestCase):

    def get_env(self):
        max_time = 30
        return Env(max_time)

    def test_attachStayCoordinates_areAttached(self):
        env = self.get_env()
        env.attachStayCoordinates(env.A)
        self.assertEqual(env.A[(2, 2)], 1)
        self.assertEqual(env.A[(17, 17)], 1)

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


if __name__ == '__main__':
    unittest.main()

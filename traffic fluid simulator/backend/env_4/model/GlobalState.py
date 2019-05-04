class GlobalState:
    def __init__(self, x, agents, A):
        self.x = x
        self.lights = [(agent.actual_phase, agent.min_phase_duration) for agent in agents]
        self.A = A

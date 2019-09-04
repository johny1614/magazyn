from typing import List

import env_settings
from Env import Env
from model.LearningState import LearningState
from services.agentFactory import get_SmartAgents

orange = 'orange'


def single_simulate(agents, actual_phase, phase_duration, den, orange_phase_duration=2, actions=[1], u=env_settings.u):
    densities: List[int] = den + [0, 0]  # dodajemy 2 ostatnie nieistotne - one sa juz na wyjsciu
    global_densities: List[int] = densities
    env = Env(agents)
    env.u = u
    state = LearningState(orange_phase_duration=orange_phase_duration,
                          actual_phase=actual_phase,
                          starting_actual_phase=actual_phase,
                          phase_duration=phase_duration,
                          global_densities=global_densities,
                          densities=densities)
    env.assign_state(state)
    env.assign_local_states_to_agents()
    env.step(actions)
    return env


def simulate_from_env(env, actions):
    env.step(actions)
    return env


agents = get_SmartAgents()
actual_phase = 0
phase_duration = 0
den = [0, 5, 10, 2]
action = [1]
env = single_simulate(agents, actual_phase, phase_duration, den, actions=action)
a = 6

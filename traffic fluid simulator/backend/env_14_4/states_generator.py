from typing import List

from Env import Env
from model.LearningState import LearningState
from services.agentFactory import get_SmartAgents

orange = 'orange'


def single_simulate(agents, actual_phase, phase_duration, den, orange_phase_duration=2):
    densities: List[int] = den + [0, 0]  # dodajemy 2 ostatnie nieistotne
    global_densities: List[int] = densities
    env = Env(agents)
    state = LearningState(orange_phase_duration=orange_phase_duration,
                          actual_phase=actual_phase,
                          starting_actual_phase=actual_phase,
                          phase_duration=phase_duration,
                          global_densities=global_densities,
                          densities=densities)
    env.assign_state(state)
    env.step([1])


agents = get_SmartAgents()
actual_phases = [0, 1, orange]
phase_durations = range(0, 5)
dens0 = dens1 = dens2 = dens3 = range(20)
for actual_phase in actual_phases:
    for phase_duration in phase_durations:
        print(phase_duration)
        for den0 in dens0:
            for den1 in dens1:
                for den2 in dens2:
                    for den3 in dens3:
                        den = [den0, den1, den2, den3]
                        single_simulate(agents, actual_phase, phase_duration, den)
a = 33

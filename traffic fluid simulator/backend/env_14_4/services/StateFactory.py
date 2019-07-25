import random
from model.LearningState import LearningState


def get_random_learning_state():
    pre_cross_densities = (random.randint(0, 30), random.randint(0, 30), random.randint(0, 30))
    global_aggregated_densities = ()
    for i in range(12):
        global_aggregated_densities = global_aggregated_densities + (random.randint(0, 60),)
    phase_index: int = random.randint(0, 4)
    phase_duration: int = random.randint(0, 15)
    ls = LearningState(pre_cross_densities, global_aggregated_densities, phase_index, phase_duration)
    return ls
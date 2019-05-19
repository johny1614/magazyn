from model import LearningState


def dist(s1: LearningState, s2: LearningState):
    distance = 0
    for i in range(len(s1.pre_cross_densities)):
        distance += 0.5*abs(s1.pre_cross_densities[i] - s2.pre_cross_densities[i])
    for i in range(len(s1.global_aggregated_densities)):
        distance += 0.1*abs(s1.global_aggregated_densities[i] - s2.global_aggregated_densities[i])
    distance += abs(s1.phase_index - s2.phase_index)
    distance += abs(s1.phase_duration - s2.phase_duration)
    return distance

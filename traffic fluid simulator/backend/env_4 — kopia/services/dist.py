import numpy as np

from model import LearningState


def dist_arr(s1_arr, s2_arr):
    distance = 0.5 * sum([abs(x-y) for x,y in zip(s1_arr[0:3],s2_arr[0:3])])
    distance += 0.1 * sum([abs(x-y) for x,y in zip(s1_arr[3:15],s2_arr[3:15])])
    distance += abs(s1_arr[15] - s2_arr[15])
    distance += abs(s1_arr[16] - s2_arr[16])
    return distance

def dist_arr_np(s1_arr, s2_arr):
    distance = 0.5 * sum(abs(s1_arr[0:3] - s2_arr[0:3]))
    distance += 0.1 * sum(abs(s1_arr[3:15] - s2_arr[3:15]))
    distance += abs(s1_arr[15] - s2_arr[15])
    distance += abs(s1_arr[16] - s2_arr[16])
    return distance

def dist(s1: LearningState, s2: LearningState):
    distance = 0
    for i in range(len(s1.pre_cross_densities)):
        distance += 0.5 * abs(s1.pre_cross_densities[i] - s2.pre_cross_densities[i])
    for i in range(len(s1.global_aggregated_densities)):
        distance += 0.1 * abs(s1.global_aggregated_densities[i] - s2.global_aggregated_densities[i])
    distance += abs(s1.phase_index - s2.phase_index)
    distance += abs(s1.phase_duration - s2.phase_duration)
    return distance

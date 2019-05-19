import random
from typing import Tuple, List

import numpy as np

from model.LearningState import LearningState
from nn_data import S1
from services.dist import dist


class Cluster:
    def __init__(self, index):
        self.index = index
        self.states: List[LearningState] = []
        self.pending_states: List[LearningState] = []
        # self.centroid: LearningState = self.get_radom_learning_state()

    @property
    def centroid(self):
        if len(self.states)+len(self.pending_states) == 0:
            return self.get_radom_learning_state()
        all_states = self.states+self.pending_states
        all_arr_states = [state.to_array() for state in all_states]
        arr_state = []
        for i in range(len(all_arr_states[0])):
            mean_of_i_coordinate=np.mean([x[i] for x in all_arr_states])
            # mean_of_i_coordinate = np.mean(all_states[i])
            arr_state.append(mean_of_i_coordinate)
        return LearningState.from_array(arr_state)

    def delete_states(self):
        self.states: List[LearningState] = []

    @staticmethod
    def get_radom_learning_state():
        pre_cross_densities = (random.randint(0, 5), random.randint(0, 5), random.randint(0, 5))
        global_aggregated_densities = ()
        for i in range(12):
            global_aggregated_densities = global_aggregated_densities + (random.randint(0, 10),)
        phase_index: int = random.randint(0, 4)
        phase_duration: int = random.randint(0, 15)
        ls = LearningState(pre_cross_densities, global_aggregated_densities, phase_index, phase_duration)
        return ls


class StateMap:
    def __init__(self, clusters_number):
        self.states: List[LearningState] = []
        self.clusters: List[Cluster] = [Cluster(index) for index in range(clusters_number)]

    def add_state(self, state: LearningState):
        state.cluster_index = self.get_cluster(state).index
        self.states.append(state)

    def get_cluster(self, state):
        closest_cluster = self.clusters[0]
        closes_distance = 99999999
        for cluster in self.clusters:
            distance = dist(state, cluster.centroid)
            if (distance < closes_distance):
                closes_distance = distance
                closest_cluster = cluster
        return closest_cluster

    def update_clusters(self):
        for cluster in self.clusters:
            cluster.delete_states()
        while True:
            states_updated = 0
            for state in self.states:
                cluster = self.get_cluster(state)
                if cluster.index != state.cluster_index:
                    states_updated += 1
                state.cluster_index = cluster.index
                cluster.pending_states.append(state)
            if states_updated == 0:
                print('zero!',states_updated)
                for state in self.states:
                    self.clusters[state.cluster_index].states.append(state)
                return
            else:
                for cluster in self.clusters:
                    cluster.pending_states=[]
            print('updates',states_updated)

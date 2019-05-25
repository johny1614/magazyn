import random
from typing import Tuple, List
import time
import numpy as np

from model.LearningState import LearningState
from nn_data import S1
from services.dist import dist

cluster_index = int


class Cluster:
    def __init__(self, index):
        self.index = index
        self.states: List[LearningState] = []
        self.states_to_remove: List[LearningState] = []
        # self.centroid: LearningState = self.get_radom_learning_state()
        self.random_centroid = self.get_radom_learning_state()

    @property
    def centroid(self):
        if len(self.states) == 0:
            return self.random_centroid
        all_arr_states = [state.to_array() for state in self.states]
        arr_state = []
        for i in range(len(all_arr_states[0])):
            mean_of_i_coordinate = np.mean([x[i] for x in all_arr_states])
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
        self.min_distance: float = 2.5  # jesli state jest dalej od kazdego centroidu o conajmniej min_distance, to powstaje nowy klaster
        self.max_clusters: int = 30  # maksymalna liczba klastrow
        self.last_epoch_states: List[LearningState] = []

    def add_state(self, state: LearningState):
        state.cluster_index = self.get_cluster(state).index
        self.states.append(state)
        self.clusters[state.cluster_index].states.append(state)

    def get_cluster(self, state):
        closest_cluster = self.clusters[0]
        closes_distance = 99999999
        for cluster in self.clusters:
            distance = dist(state, cluster.centroid)
            if (distance < closes_distance):
                closes_distance = distance
                closest_cluster = cluster
        if (closes_distance > self.min_distance and len(self.clusters) <= self.max_clusters):
            new_cluster = Cluster(len(self.clusters))
            self.clusters.append(new_cluster)
            closest_cluster = new_cluster
        return closest_cluster

    def update_clusters(self):
        # print('liczba stanow to',len(self.states))
        start = time.time();
        while True:
            states_updated = 0
            for cluster in self.clusters:
                for state in cluster.states:
                    new_cluster = self.get_cluster(state)
                    if new_cluster != cluster:
                        states_updated += 1
                        state.cluster_index = new_cluster.index
                        cluster.states_to_remove.append(state)
                        new_cluster.states.append(state)
            for cluster in self.clusters:
                for state_to_remove in cluster.states_to_remove:
                    cluster.states.remove(state_to_remove)
                cluster.states_to_remove = []
            if states_updated < 0.05*len(self.states):
                end = time.time();
                print('czas to',(end-start))
                return
            # print('states_updated',states_updated)

    def activate_unused_clusters(self):
        unused_clusters = [cluster for cluster in self.clusters if len(cluster.states) > 0]
        for unused_cluster in unused_clusters:
            unused_cluster.random_centroid = Cluster.get_radom_learning_state()

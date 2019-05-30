from typing import List

from StateMap import Cluster, StateMap
from model.LearningState import LearningState
import random

states: List[LearningState] = [Cluster.get_radom_learning_state() for x in range(900)]
states_map = StateMap(10)
for state in states:
    state.cluster_index = random.randint(0,9)
    states_map.clusters[state.cluster_index].states.append(state)
states_map.states = states
states_map.last_epoch_states=states
states_map.update_clusters()

from typing import Tuple, Dict, List
import attr
import numpy as np

from model.Action import Action
from model.Agent import Agent
from model.LearningState import LearningState
import random

from StateMap import StateMap
from services.globals import Globals


def empty_dic():
    return {}


@attr.s(auto_attribs=True)
class SmartAgent(Agent):
    returns: Dict[Tuple[LearningState, Action], List[float]] = attr.ib(default=attr.Factory((empty_dic)))
    Q: Dict[Tuple[int,Action],float] = attr.ib(default=attr.Factory((empty_dic)))
    pi: Dict[int, Action] = attr.ib(default=attr.Factory((empty_dic)))
    states_map = StateMap(10)

    def get_action_according_to_pi(self, learning_state: LearningState, random_probabilty: float) -> Action:
        if (random_probabilty):
            rand_value = random.random()
            if (rand_value < random_probabilty):
                return random.choice(list(self.local_action_space))
        if learning_state not in self.pi:
            random_action = random.choice(list(self.local_action_space))
            self.pi[learning_state.cluster_index] = random_action
        if self.pi[learning_state.cluster_index] not in self.local_action_space:
            return random.choice(list(self.local_action_space))
        return self.pi[learning_state.cluster_index]

    def add_states_to_map_state(self):
        for state in self.epoch_local_state_storage:
            self.states_map.add_state(state)

    def print_used_states(self):
        used=0
        for cluster in self.states_map.clusters:
            # print(cluster.states)
            if len(cluster.states)>2:
                used+=1
        print(used)
    def add_returns(self, G):
        for i in range(len(G)):
            if ((self.epoch_local_state_storage[i], self.epoch_local_action_storage[i]) in self.returns.keys()):
                self.returns[self.epoch_local_state_storage[i], self.epoch_local_action_storage[i]].append(G[i])
                Globals().state_repeats += 1
            else:
                Globals().new_states += 1
                self.returns[self.epoch_local_state_storage[i], self.epoch_local_action_storage[i]] = [G[i]]

    def update_Q(self):
        for i in range(len(self.epoch_local_state_storage)):
            state: LearningState = self.epoch_local_state_storage[i]
            action: Action = self.epoch_local_action_storage[i]
            self.Q[(state.cluster_index,action)] = np.mean(self.returns[state, action])

    def update_pi(self):
        for i in range(len(self.epoch_local_state_storage) - 1):
            state = self.epoch_local_state_storage[i]
            self.pi[state.cluster_index] = self.find_best_Q(state)

    def clear_epoch_local_data(self):
        self.epoch_local_state_storage = ()
        self.epoch_local_action_storage = ()

    def find_best_Q(self, state: LearningState):
        bestValue = -9
        bestAction = None
        q_of_state_cluster = [q_key for q_key in self.Q.keys() if q_key[0] == state.cluster_index]
        for q_key in q_of_state_cluster:
            if (self.Q[q_key] >= bestValue):
                bestValue == self.Q[q_key]
                bestAction = q_key[1]
        return bestAction

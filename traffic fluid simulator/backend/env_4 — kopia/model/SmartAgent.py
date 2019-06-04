import itertools
from typing import Tuple, Dict, List
import attr
import numpy as np

from model.Agent import Agent
from model.LearningState import LearningState
import random

from StateMap import StateMap, cluster_index
from model.Memory import Memory
from services.globals import Globals
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import random


def empty_dic():
    return {}


def state_map():
    return StateMap(10)


@attr.s
class SmartAgent(Agent):
    memories: List[Memory] = attr.ib(factory=list)
    single_epoch_memory: List[Memory] = attr.ib(factory=list)

    def __attrs_post_init__(self):
        self.model = self._build_model()

    def get_action(self, state):
        # TODO z sieci neuronowej ma brac

        if np.random.rand() <= Globals().epsilon():  # if acting randomly, take random action
            return random.choice(self.local_action_space)
        act_values = self.model.predict(
            state.to_nd_array())  # if not acting randomly, predict reward value based on current state
        action = np.argmax(act_values[0])
        if action not in self.local_action_space:
            sorted_actions = np.argsort(-act_values[0])
            for a in sorted_actions:
                if a in self.local_action_space:
                    return action
        return action

        # return random.choice(self.local_action_space)

    def _build_model(self):
        # neural net to approximate Q-value function:
        model = Sequential()
        model.add(Dense(24, input_dim=17, activation='relu'))  # 1st hidden layer; states as input
        model.add(Dense(24, activation='relu'))  # 2nd hidden layer
        model.add(Dense(4, activation='linear'))  # 2 actions, so 2 output neurons: 0 and 1 (L/R)
        model.compile(loss='mse',
                      optimizer=Adam(lr=Globals().learning_rate))
        return model

    def train(self):
        gamma = Globals().gamma
        batch_size = Globals().batch_size
        minibatch = random.sample(self.memories, batch_size)
        for memory in minibatch:
            state = memory.state.to_nd_array()
            new_state = memory.new_state.to_nd_array()
            target = (memory.reward + gamma *  # (target) = reward + (discount rate gamma) *
                      np.amax(self.model.predict(new_state)))  # (maximum target Q based on future action a')
            actual_result_net = self.model.predict(state)
            actual_result_net[0][memory.action] = target
            self.model.fit(state, actual_result_net, epochs=Globals().epochs_learn, verbose=0)
        self.single_epoch_memory=[]

    def remember(self, densities):
        state = self.local_state
        action = self.action
        self.assign_local_state(densities)
        new_state = self.local_state
        reward = self.count_reward(state, new_state)
        memory = Memory(state=state, action=action, new_state=new_state, reward=reward)
        self.memories.append(memory)
        self.single_epoch_memory.append(memory)

    def count_reward(self, state, new_state):
        return new_state.pre_cross_densities[2] - state.pre_cross_densities[2]

    # returns: Dict[Tuple[LearningState, Action], List[float]] = attr.ib(default=attr.Factory((empty_dic)))
    # Q: Dict[Tuple[cluster_index, Action], float] = attr.ib(default=attr.Factory((empty_dic)))
    # pi: Dict[int, Action] = attr.ib(default=attr.Factory((empty_dic)))
    # states_map: StateMap = attr.ib(default=attr.Factory((state_map)))
    #
    # def get_action_according_to_pi(self, learning_state: LearningState, random_probabilty: float) -> Action:
    #     if (random_probabilty):
    #         rand_value = random.random()
    #         if (rand_value < random_probabilty):
    #             return random.choice(list(self.local_action_space))
    #     if learning_state not in self.pi:
    #         random_action = random.choice(list(self.local_action_space))
    #         self.pi[learning_state.cluster_index] = random_action
    #     if self.pi[learning_state.cluster_index] not in self.local_action_space:
    #         return random.choice(list(self.local_action_space))
    #     return self.pi[learning_state.cluster_index]
    #
    # def add_states_to_map_state(self):
    #     for state in self.epoch_local_state_storage:
    #         self.states_map.add_state(state)
    #     self.states_map.last_epoch_states = self.epoch_local_state_storage
    #
    # def print_used_states(self):
    #     used = 0
    #     for cluster in self.states_map.clusters:
    #         # print(cluster.states)
    #         if len(cluster.states) > 2:
    #             used += 1
    #     print(used)
    #
    # def add_returns(self, G):
    #     for i in range(len(G)):
    #         if ((self.epoch_local_state_storage[i], self.epoch_local_action_storage[i]) in self.returns.keys()):
    #             self.returns[self.epoch_local_state_storage[i], self.epoch_local_action_storage[i]].append(G[i])
    #             Globals().state_repeats += 1
    #         else:
    #             Globals().new_states += 1
    #             self.returns[self.epoch_local_state_storage[i], self.epoch_local_action_storage[i]] = [G[i]]
    #
    # def update_Q(self):
    #     for i in range(len(self.epoch_local_state_storage)):
    #         state: LearningState = self.epoch_local_state_storage[i]
    #         action: Action = self.epoch_local_action_storage[i]
    #         key_returns_of_cluster_action_pair = [ret for ret in self.returns if
    #                                               ret[0].cluster_index == state.cluster_index and ret[1] == action]
    #         values_returns_of_cluster_action_pair = [self.returns[key] for key in key_returns_of_cluster_action_pair]
    #         flat_values = list(itertools.chain.from_iterable(values_returns_of_cluster_action_pair))
    #         self.Q[(state.cluster_index, action)] = np.mean(flat_values)
    #         # appearance = len(flat_values)
    #         # print('update q na podstawie ilosci par klaster-akcja', appearance)
    #
    # def update_pi(self):
    #     for i in range(len(self.epoch_local_state_storage) - 1):
    #         state = self.epoch_local_state_storage[i]
    #         self.pi[state.cluster_index] = self.find_best_Q(state)
    #
    # def clear_epoch_local_data(self):
    #     self.epoch_local_state_storage = ()
    #     self.epoch_local_action_storage = ()
    #
    # def find_best_Q(self, state: LearningState):
    #     bestValue = -9
    #     bestAction = None
    #     q_of_state_cluster = [q_key for q_key in self.Q.keys() if q_key[0] == state.cluster_index]
    #     for q_key in q_of_state_cluster:
    #         if (self.Q[q_key] >= bestValue):
    #             bestValue == self.Q[q_key]
    #             bestAction = q_key[1]
    #     return bestAction

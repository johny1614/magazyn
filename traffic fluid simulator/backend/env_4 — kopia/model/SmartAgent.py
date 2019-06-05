import itertools
from typing import Tuple, Dict, List
import attr
import numpy as np
from tensorflow.python.keras.layers import BatchNormalization
from tensorflow.python.keras.utils import plot_model
import matplotlib.pyplot as plt

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

    def __attrs_post_init__(self):
        self.model = self._build_model()

    def get_action(self, state):
        if np.random.rand() <= Globals().epsilon():  # if acting randomly, take random action
            return random.choice(self.local_action_space)
        act_values = self.model.predict(
            state.to_learn_nd_array())  # if not acting randomly, predict reward value based on current state
        action = np.argmax(act_values[0])
        if action not in self.local_action_space:
            sorted_actions = np.argsort(-act_values[0])
            for a in sorted_actions:
                if a in self.local_action_space:
                    return action
        return int(action) # sometimes jump to int64

        # return random.choice(self.local_action_space)

    def _build_model(self):
        # neural net to approximate Q-value function:
        model = Sequential()
        model.add(Dense(12, input_dim=5, activation='relu'))  # 1st hidden layer; states as input
        model.add(BatchNormalization())
        model.add(Dense(10, activation='relu'))  # 2nd hidden layer
        model.add(Dense(4, activation='linear'))  # 2 actions, so 2 output neurons: 0 and 1 (L/R)
        model.compile(loss='mse',
                      optimizer=Adam(lr=Globals().learning_rate))
        return model

    def train(self):
        gamma = Globals().gamma
        batch_size = Globals().batch_size
        minibatch = random.sample(self.memories, batch_size)
        for memory in minibatch:
            state = memory.state.to_learn_nd_array()
            new_state = memory.new_state.to_learn_nd_array()
            target = (memory.reward + gamma *  # (target) = reward + (discount rate gamma) *
                      np.amax(self.model.predict(new_state)))  # (maximum target Q based on future action a')
            actual_result_net = self.model.predict(state)
            actual_result_net[0][memory.action] = target


    def remember(self, densities,reward):
        state = self.local_state
        action = self.action
        self.assign_local_state(densities)
        new_state = self.local_state
        times = {'old':Globals().time-1,'new':Globals().time}
        memory = Memory(state=state, action=action, new_state=new_state, reward=reward,times=times)
        self.memories.append(memory)

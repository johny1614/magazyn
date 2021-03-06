import itertools
import math
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
        self.private_model = self._build_model()

    def get_action(self, state):
        if np.random.rand() <= Globals().epsilon():  # if acting randomly, take random action
            action =random.choice(self.local_action_space)
            # if self.index == 0 and Globals().time == 14:
            #     print(f'stan {state.to_learn_nd_array()} i losowa akcja: {action} ')
            return action
        predictions = self.model.predict(
            state.to_learn_nd_array())  # if not acting randomly, predict reward value based on current state
        if self.index == 0 and Globals().time == 14:
            print(f'predictions {predictions[0]} dla stanu {state.to_learn_nd_array()}')
        action = np.argmax(predictions[0])
        if action not in self.local_action_space:
            sorted_actions = np.argsort(-predictions[0])
            for a in sorted_actions:
                if a in self.local_action_space:
                    return int(a)
        return int(action)  # sometimes jump to int64

        # return random.choice(self.local_action_space)

    def _build_model(self):
        # neural net to approximate Q-value function:
        model = Sequential()
        # model.add(Dense(Globals().l1, input_dim=3, activation='relu'))  # 1st hidden layer; states as input
        # model.add(BatchNormalization())
        # model.add(Dense(Globals().l2, activation='relu'))  # 2nd hidden layer
        # model.add(Dense(Globals().l3, activation='relu'))  # 2nd hidden layer
        # model.add(Dense(4, activation='linear'))  # 2 actions, so 2 output neurons: 0 and 1 (L/R)

        model.add(Dense(10, input_dim=3, activation='relu'))  # 1st hidden layer; states as input
        model.add(Dense(20, activation='relu'))
        model.add(Dense(4, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=Globals().learning_rate))
        return model

    def train(self):
        gamma = Globals().gamma
        batch_size = Globals().batch_size
        minibatch = self.memories[-90:]
        # minibatch = self.memories
        # minibatch = random.sample(self.memories, batch_size)
        i = 0
        artificial_state = [6, 1, 1]
        artifical_y = [0, 0, 1000000, 0]
        x_batch = []
        y_batch = []
        for memory in minibatch:
            # if self.index != 0:
            #     if 14 != i:
            #         i+=1
            #         continue
            state = memory.state.to_learn_nd_array()
            new_state = memory.new_state.to_learn_nd_array()
            y_target = self.model.predict(state)
            target = (memory.reward + gamma *  # (target) = reward + (discount rate gamma) *
                      np.amax(self.model.predict(new_state)))  # (maximum target Q based on future action a')
            y_target[0][memory.action] = target
            x_batch.append(state[0])
            y_batch.append(y_target[0])
            # if self.index == 0:
            #     if 14 == i:
            #         # print(f'time {i} state {state} action {memory.action} reward {memory.reward} y_target {y_target[0]} dla akcji {y_target[0][memory.action]}')
            #         private_x_batch = [state[0]]
            #         private_y_batch = [y_target[0]]
            #         Globals().x_batch.append(state[0])
            #         Globals().y_batch.append(y_target[0])
            #         self.private_model.fit(np.array(Globals().x_batch),np.array(Globals().y_batch),epochs=100,validation_split=0.2,verbose=0)
            #         pred = self.private_model.predict(np.array([[6, 1, 1]]))
            #         print(pred)
            #         # self.private_model.evaluate(x=np.array(Globals().x_batch),y=np.array(Globals().y_batch))
            # i += 1
        self.model.fit(np.array(x_batch), np.array(y_batch),epochs=100, batch_size=len(x_batch), verbose=0)

    def remember(self, densities, reward):
        state = self.local_state
        action = self.action
        self.assign_local_state(densities)
        new_state = self.local_state
        times = {'old': Globals().time - 1, 'new': Globals().time}
        memory = Memory(state=state, action=action, new_state=new_state, reward=reward, times=times)
        self.memories.append(memory)

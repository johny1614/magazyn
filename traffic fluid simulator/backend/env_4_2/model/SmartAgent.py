import itertools
import math
from typing import Tuple, Dict, List
import attr
import numpy as np
from tensorflow.python.keras.layers import BatchNormalization
from tensorflow.python.keras.losses import huber_loss
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
            # print(f'{self.local_action_space} bo phase_duration {self.phase_duration}')
            action = random.choice(self.local_action_space)
            # TODO tutaj losuje zera!
            # print(action)
            # if self.index == 0 and Globals().time == 14:
            #     print(f'stan {state.to_learn_nd_array()} i losowa akcja: {action} ')
            return action
        predictions = self.model.predict(
            state.to_learn_nd_array_full())  # if not acting randomly, predict reward value based on current state
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
        model.add(Dense(70, input_dim=37, activation='relu'))  # 1st hidden layer; states as input
        # model.add(BatchNormalization())

        # 70, 100, 150, 100, 80, 60, 30
        model.add(Dense(100, activation='relu'))
        model.add(Dense(150, activation='relu'))
        model.add(Dense(100, activation='relu'))
        model.add(Dense(80, activation='relu'))
        model.add(Dense(60, activation='relu'))
        model.add(Dense(30, activation='relu'))
        model.add(Dense(4, activation='linear'))
        model.compile(loss=huber_loss,
                      optimizer=Adam())
        return model

    def save_batch(self):
        gamma = Globals().gamma
        batch_size = Globals().batch_size
        # minibatch = random.sample(self.memories, batch_size)
        x_batch = []
        y_batch = []
        i = 0
        for memory in self.memories:
            if memory.action == 0:
                continue
            i += 1
            state = memory.state.to_learn_nd_array_full()
            new_state = memory.new_state.to_learn_nd_array_full()
            y = self.model.predict(state)
            future_actions_values_predictions = self.model.predict(new_state)
            possible_actions = memory.state.possible_actions(self.orange_phase_duration)
            best_possible_future_action_value = np.amax(
                [future_actions_values_predictions[0][i] for i in possible_actions])
            target_action = (memory.reward + gamma *  # (target) = reward + (discount rate gamma) *
                             best_possible_future_action_value)  # (maximum target Q based on future action a')
            # so this is the q value for action made in state leading to new_state
            # counted basing on - reward and reward of future best action
            y[0][memory.action] = target_action
            x_batch.append(state[0])
            y_batch.append(y[0])
            if self.index == 0:
                Globals().x_batch.append(state[0])
                Globals().y_batch.append(y[0])

    def memory_to_minibatch(self, batch_size):
        gamma = Globals().gamma
        minibatch = random.sample(self.memories, min(len(self.memories), batch_size))
        x_batch = []
        y_batch = []
        for memory in minibatch:
            state = memory.state.to_learn_nd_array_full()
            new_state = memory.new_state.to_learn_nd_array_full()
            y_target = self.model.predict(state)
            target = (memory.reward + gamma *  # (target) = reward + (discount rate gamma) *
                      np.amax(self.model.predict(new_state)))  # (maximum target Q based on future action a')
            y_target[0][memory.action] = target
            x_batch.append(state[0])
            y_batch.append(y_target[0])
        return x_batch, y_batch

    def train(self):
        batch_size = Globals().batch_size
        val_batch_size = Globals().validation_batch_size
        x_batch, y_batch = self.memory_to_minibatch(batch_size)
        x_val_batch, y_val_batch = self.memory_to_minibatch(val_batch_size)
        # validation_batch_size = Globals().validation_batch_size
        # validation_batch = random.sample(self.memories, min(len(self.memories), validation_batch_size))
        i=9
        if self.index == 0:
            val_loss = 999999999
            while True:
                i+=10
                res = self.model.fit(np.array(x_batch), np.array(y_batch), epochs=10, batch_size=len(x_batch),
                                     verbose=0)
                validation = self.model.evaluate(np.array(x_val_batch), np.array(y_val_batch),verbose=0)
                if validation > val_loss:
                    print(f'agent {self.index} po {10} epochach ma  {validation}')
                    break
                val_loss = validation
                # y_pred = self.model.predict([x_batch[0:10]])
                x = [0, 0, 60] + [0] * 33 + [1]
                print(self.model.predict(np.array([x])))
                # val_loss = self.model.evaluate()

                # i = 2

    def remember(self, densities, reward):
        state = self.local_state
        action = self.action
        self.assign_local_state(densities)
        new_state = self.local_state
        times = {'old': Globals().time - 1, 'new': Globals().time}
        memory = Memory(state=state, action=action, new_state=new_state, reward=reward, times=times)
        # if self.index ==0:
        #     print(memory)
        self.memories.append(memory)

    def reshape_rewards(self):
        for i in range(len(self.memories) - 3):
            memory = self.memories[i]
            future_rewards = [mem.reward for mem in self.memories[i + 1:i + 3]]  # 2 next rewards
            if i == 60:
                print(future_rewards)
            memory.reward += sum(future_rewards)
            self.memories[i] = memory

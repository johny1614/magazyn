import random
from typing import List

import attr
import numpy as np
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam

from model.Agent import Agent
from model.Memory import Memory
from services.globals import Globals


def empty_dic():
    return {}


@attr.s
class SmartAgent(Agent):
    memories: List[Memory] = attr.ib(factory=list)

    def __attrs_post_init__(self):
        self.model = self._build_model([20, 50, 30, 18])

    def get_action(self, state):
        if state.actual_phase == 'orange':
            return 'orange'
        if np.random.rand() <= Globals().epsilon:  # if acting randomly, take random action
            # print(f'{self.local_action_space} bo phase_duration {self.phase_duration}')
            action = random.choice(self.local_action_space)
            # TODO tutaj losuje zera!
            # print(action)
            # if self.index == 0 and Globals().time == 14:
            #     print(f'stan {state.to_learn_nd_array()} i losowa akcja: {action} ')
            return action
        predictions = self.model.predict(
            state.to_9_densities_learn_array())  # if not acting randomly, predict reward value based on current state
        action = np.argmax(predictions[0])
        if action not in self.local_action_space:
            sorted_actions = np.argsort(-predictions[0])
            for a in sorted_actions:
                if a in self.local_action_space:
                    return int(a)
        return int(action)  # sometimes jump to int64

        # return random.choice(self.local_action_space)

    def _build_model(self, layers):
        # neural net to approximate Q-value function:
        model = Sequential()
        model.add(Dense(layers[0], input_dim=10, activation='relu'))  # 1st hidden layer; states as input
        for layer in layers[1:]:
            model.add(Dense(layer, activation='relu'))
        model.add(Dense(3, activation='linear'))
        model.compile(loss='mse',
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
            if memory.action == 'orange':
                continue
            i += 1
            state = memory.state.to_9_densities_learn_array()
            new_state = memory.new_state.to_9_densities_learn_array()
            y = self.model.predict(state)
            target_action = memory.reward
            # target_action = (memory.reward + gamma *  # (target) = reward + (discount rate gamma) *
            #                  best_possible_future_action_value)  # (maximum target Q based on future action a')
            # so this is the q value for action made in state leading to new_state
            # counted basing on - reward and reward of future best action
            y[0][memory.action] = target_action
            x_batch.append(state[0])
            y_batch.append(y[0])
            if self.index == 0:
                Globals().x_batch.append(state[0])
                Globals().y_batch.append(y[0])

    def random_minibatch(self, batch_size):
        minibatch = random.sample(self.memories, min(len(self.memories), batch_size))
        x_batch = []
        y_batch = []
        for memory in minibatch:
            if memory.action == 'orange':
                continue
            state = memory.state.to_9_densities_learn_array()
            y_target = self.model.predict(state)
            target = (memory.reward)
            y_target[0][memory.action] = target
            x_batch.append(state[0])
            y_batch.append(y_target[0])
        return x_batch, y_batch
    def memory_to_minibatch_with_oranges(self, memories=None):
        memories = self.memories if memories is None else None
        gamma = Globals().gamma
        x_batch = []
        y_batch = []
        for memory in memories:
            if memory.state.starting_actual_phase=='orange':
                x_batch.append(state[0])
                y_batch.append('orange')
                continue
            state = memory.state.to_9_densities_learn_array()
            y_target = self.model.predict(state)
            target = (memory.reward)
            y_target[0][memory.action] = target
            x_batch.append(state[0])
            y_batch.append(y_target[0])
        return x_batch, y_batch

    def memory_to_minibatch(self, memories=None):
        memories = self.memories if memories is None else None
        gamma = Globals().gamma
        x_batch = []
        y_batch = []
        for memory in memories:
            if memory.state.starting_actual_phase=='orange':
                continue
            state = memory.state.to_9_densities_learn_array()
            y_target = self.model.predict(state)
            target = (memory.reward)
            y_target[0][memory.action] = target
            x_batch.append(state[0])
            y_batch.append(y_target[0])
        return x_batch, y_batch

    def train_good_memes(self):
        x_batch, y_batch = self.memory_to_minibatch(Globals().goodmemes)
        res = self.model.fit(np.array(x_batch), np.array(y_batch), epochs=10, batch_size=len(x_batch),
                             verbose=0)
        x = [0, 0, 60] + [0] * 33 + [1]
        print(self.model.predict(np.array([x])))

    def full_batch(self):
        x_batch = []
        y_batch = []
        gamma = Globals().gamma
        for memory in self.memories:
            state = memory.state.to_9_densities_learn_array()
            if state[0][-1] == 'orange':
                continue
            y_target = self.model.predict(state)
            target = (memory.reward)
            y_target[0][memory.action] = target
            x_batch.append(state[0])
            y_batch.append(y_target[0])
        return x_batch, y_batch

    def train_full(self, epochs=20, learning_rate=0.0001):
        # batch_size = Globals().batch_size
        # val_batch_size = Globals().validation_batch_size
        x_batch, y_batch = self.full_batch()
        self.model.learning_rate = learning_rate
        res = self.model.fit(np.array(x_batch), np.array(y_batch), epochs=epochs, batch_size=len(x_batch),
                             verbose=0)

    def evaluate_full(self):
        x_batch, y_batch = self.full_batch()
        return self.model.evaluate(np.array(x_batch), np.array(y_batch), verbose=0)

    def train(self, batch_size=Globals().batch_size, epochs=20, learning_rate=0.0001):
        x_batch, y_batch = self.random_minibatch(batch_size)
        self.model.learning_rate = learning_rate
        res = self.model.fit(np.array(x_batch), np.array(y_batch), epochs=epochs, batch_size=len(x_batch), verbose=0)
        # print(res.history['loss'][-1])

    def remember(self, densities, reward):
        state = self.local_state
        action = self.action
        self.assign_local_state(densities)
        new_state = self.local_state
        times = {'old': Globals().time - 1, 'new': Globals().time}
        memory = Memory(state=state, action=action, new_state=new_state, reward=reward, times=times)
        # if if self.index ==0:
        #     print(memory)
        self.memories.append(memory)

    def reshape_rewards(self):
        for i in range(len(self.memories) - 3):
            memory = self.memories[i]
            if not memory.reshapedReward:
                memory.reshapedReward = True
                future_rewards = [mem.reward for mem in self.memories[i + 1:i + 3]]  # 2 next rewards
                memory.reward += sum(future_rewards)
                self.memories[i] = memory

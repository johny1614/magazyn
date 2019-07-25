import random
from statistics import mean
from typing import List
import attr
import numpy as np
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.python.keras import regularizers
from tensorflow.python.keras.layers import Activation

from env_settings import max_time
from model.Agent import Agent
from model.Memory import Memory
from services.globals import Globals


@attr.s
class SmartAgent(Agent):
    memories: List[Memory] = attr.ib(factory=list)
    model = attr.ib(default=0)

    def __attrs_post_init__(self):
        if self.model == 0:
            l_rate = Globals().vp().nn_l_rate
            layers = Globals().vp().layers
            activation = 'relu'
            self.model = self._build_model(layers=layers, activation=activation, l_rate=l_rate)

    def _build_model(self, layers, activation='relu', l_rate=0.01, reg_val=Globals().vp().regularization):
        model = Sequential()
        for i, nodes in enumerate(layers):
            if i == 0:
                model.add(Dense(nodes, input_dim=8, activation='linear'))
            else:
                model.add(Dense(nodes, kernel_regularizer=regularizers.l2(reg_val)))
                model.add(Activation(activation))
        model.add(Dense(3))
        model.compile(optimizer=Adam(learning_rate=l_rate), loss='mse')
        return model

    def random_minibatch(self, batch_size):
        minibatch = random.sample(self.memories, min(len(self.memories), batch_size))
        x_batch = []
        y_batch = []
        for memory in minibatch:
            if memory.action == 'orange':
                continue
            state = memory.state.to_learn_array()
            y_target = self.model.predict(state)
            target = (memory.reward)
            y_target[0][memory.action] = target
            x_batch.append(state[0])
            y_batch.append(y_target[0])
        return x_batch, y_batch

    def full_batch(self,only_learn_usable = False):
        x_batch = []
        y_batch = []
        i = 0
        l_rate = Globals().learning_rate
        gamma = Globals().vp().gamma
        memories = self.memories if not only_learn_usable else [mem for mem in self.memories if mem.learn_usable]
        for memory in memories:
            state = memory.state.to_learn_array()
            action = 2 if memory.action == 'orange' else memory.action
            y_target = self.model.predict(state)
            new_state_possible_actions_value_predictions = self.model.predict(memory.new_state.to_learn_array())
            target = (1 - l_rate) * y_target[0][action] + l_rate * (
                    memory.reward + gamma * max(new_state_possible_actions_value_predictions[0]))
            i += 1
            y_target[0][action] = target
            x_batch.append(state[0])
            y_batch.append(y_target[0])
        return x_batch, y_batch

    def train_full(self, epochs=20, learning_rate=0.0001):
        x_batch, y_batch = self.full_batch(only_learn_usable=True)
        self.model.learning_rate = learning_rate
        res = self.model.fit(np.array(x_batch), np.array(y_batch), epochs=epochs, batch_size=len(x_batch),
                             verbose=0)

    def train(self, batch_size=Globals().batch_size, epochs=20, learning_rate=0.0001):
        x_batch, y_batch = self.random_minibatch(batch_size)
        self.model.learning_rate = learning_rate
        res = self.model.fit(np.array(x_batch), np.array(y_batch), epochs=epochs, batch_size=len(x_batch),
                             verbose=0)

    def get_action(self, state):
        if state.actual_phase == 'orange':
            return 'orange'
        if np.random.rand() <= Globals().epsilon:  # if acting randomly, take random action
            action = random.choice(self.local_action_space)
            return action
        predictions = self.model.predict(
            state.to_learn_array())  # if not acting randomly, predict reward value based on current state
        action = np.argmax(predictions[0])
        if action not in self.local_action_space:
            sorted_actions = np.argsort(-predictions[0])
            for a in sorted_actions:
                if a in self.local_action_space:
                    return int(a)
        return int(action)  # sometimes jump to int64

    def remember(self, densities, reward):
        state = self.local_state
        action = self.action
        self.assign_local_state(densities)
        new_state = self.local_state
        times = {'old': Globals().time - 1, 'new': Globals().time}
        memory = Memory(state=state, action=action, new_state=new_state, reward=reward, times=times,
                        epoch_index=Globals().actual_epoch_index)
        self.memories.append(memory)

    def last_epoch_batch(self):
        return self.memories[-90:]

    def reshape_rewards(self):
        for i in range(len(self.memories)):  # - Globals().vp().reshape_future
            memory = self.memories[i]
            if i in range(max_time-Globals().not_to_learn_last_epochs,max_time):
                memory.reshapedReward=True
                memory.learn_usable = False
            if not memory.reshapedReward:
                memory.reshapedReward = True
                furute_memories = [mem for mem in self.memories[i + 1:i + 1 + Globals().vp().reshape_future] if mem.epoch_index==memory.epoch_index]
                if len(furute_memories) < Globals().vp().reshape_future:
                    memory.learn_usable = False
                    continue
                memory.reward += sum([mem.reward for mem in furute_memories])
                self.memories[i] = memory
                # print('rew',memory.reward)
                # if 3 < memory.state.densities[0] < 5 and 9 < memory.state.densities[
                #     1] < 15 and memory.action == 1 and memory.state.starting_actual_phase == 1:
                #     print(f'state {memory.state.densities[0]},{memory.state.densities[1]} a:{memory.action}')
                #     print('reww', memory.reward)
                #     rew powinno byc przynajmniej 9!
                # else:
                #     print(f'state {memory.state.densities[0]},{memory.state.densities[1]} a:{memory.action}')

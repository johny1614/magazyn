import random
from typing import List
import attr
import numpy as np
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.python.keras.layers import Activation
from model.Agent import Agent
from model.Memory import Memory
from services.globals import Globals


@attr.s
class SmartAgent(Agent):
    memories: List[Memory] = attr.ib(factory=list)
    model = attr.ib(default=0)

    def __attrs_post_init__(self):
        if self.model == 0:
            l_rate = 0.01
            layers = [10]
            activation = 'relu'
            self.model = self._build_model(layers=layers, activation=activation, l_rate=l_rate)

    def _build_model(self, layers, activation, l_rate):
        model = Sequential()
        for i, nodes in enumerate(layers):
            if i == 0:
                model.add(Dense(nodes, input_dim=2, activation=activation))
            else:
                model.add(Dense(nodes))
                model.add(Activation(activation))
        model.add(Dense(2))
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

    def full_batch(self):
        x_batch = []
        y_batch = []
        i = 0
        l_rate = Globals().learning_rate
        gamma = Globals().gamma
        for memory in self.memories:
            state = memory.state.to_learn_array()
            action = 2 if memory.action == 'orange' else memory.action
            y_target = self.model.predict(state)
            new_state_possible_actions_value_predictions = self.model.predict(memory.new_state.to_learn_array())
            target = (1 - l_rate) * y_target[0][action] + l_rate * (memory.reward + gamma * max(new_state_possible_actions_value_predictions[0]))
            i += 1
            y_target[0][action] = target
            x_batch.append(state[0])
            y_batch.append(y_target[0])
        return x_batch, y_batch

    def train_full(self, epochs=20, learning_rate=0.0001):
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
        memory = Memory(state=state, action=action, new_state=new_state, reward=reward, times=times)
        self.memories.append(memory)

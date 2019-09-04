import random
from statistics import mean
from typing import List
import attr
import numpy as np
from tensorflow.keras.initializers import Constant
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.python.keras.layers import Activation
from model.Agent import Agent
from model.Memory import Memory
from services.globals import Globals


@attr.s
class SmartAgent(Agent):
    outflow_section: int = attr.ib(default=0)
    memories: List[Memory] = attr.ib(factory=list)
    model = attr.ib(default=0)
    randomed_actions = [0, 0, 0]

    def __attrs_post_init__(self):
        if self.model == 0:
            layers = Globals().vp().layers
            l_rate = Globals().vp().nn_l_rate
            self.model = self._build_model(layers=layers, l_rate=l_rate)
            a = 34

    def _build_model(self, layers, l_rate=0.01):
        model = Sequential()
        for i, nodes in enumerate(layers):
            if i == 0:
                model.add(Dense(nodes, input_dim=8, activation='relu'))
            else:
                model.add(Dense(nodes, bias_initializer='zeros'))
                model.add(Activation('relu'))
        model.add(Dense(4, bias_initializer=Constant(value=15)))
        model.compile(optimizer=Adam(learning_rate=l_rate), loss='mse')
        return model


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

    def get_action(self, state, greedy=False):
        if state.actual_phase == 'orange':
            return 'orange'
        if np.random.rand() <= Globals().epsilon and not greedy:  # if acting randomly, take random action
            action = random.choice(self.local_action_space)
            return action
        predictions = self.model.predict(
            state.to_learn_array(self))  # if not acting randomly, predict reward value based on current state
        action = np.argmax(predictions[0])
        if action not in self.local_action_space:
            sorted_actions = np.argsort(-predictions[0])
            for a in sorted_actions:
                if a in self.local_action_space:
                    return int(a)
        return int(action)  # sometimes jump to int64

    def save_batch(self):
        x_batch = []
        y_batch = []
        for memory in self.memories:
            if memory.action == 'orange':
                continue
            state = memory.state.to_learn_array(self)
            y = memory.reward
            x_batch.append(state[0])
            y_batch.append(y)
            if self.index == 0:
                Globals().x_batch.append(state[0])
                Globals().y_batch.append(y)

    def remember(self, densities, reward):
        state = self.local_state
        action = self.action
        self.assign_local_state(densities)
        new_state = self.local_state
        times = {'old': Globals().time - 1, 'new': Globals().time}
        memory = Memory(state=state, action=action, new_state=new_state, reward=reward, times=times,
                        epoch_index=Globals().actual_epoch_index)
        self.memories.append(memory)

    def full_batch_no_orange(self, only_learn_usable=True):
        x_batch = []
        y_batch = []
        l_rate = Globals().vp().q_formula_l_rate
        gamma = Globals().vp().gamma
        all_memories = self.memories
        # memories = self.memories if not only_learn_usable else [mem for mem in self.memories if mem.learn_usable]
        for i in range(len(all_memories)):
            memory = all_memories[i]
            if memory.action == 'orange' or not memory.learn_usable:
                continue
            state = memory.state.to_learn_array(self)
            action = memory.action
            y_target = self.model.predict(state)
            if not memory.holded_lights:
                if len(all_memories) < i + self.orange_phase_duration:
                    print('zle len')
                new_light_reward = all_memories[i + self.orange_phase_duration].reward
                new_state_possible_actions_value_predictions = self.model.predict(
                    all_memories[i + self.orange_phase_duration].state.to_learn_array(self))
                max_next_action_value = max(new_state_possible_actions_value_predictions[0])
                target = (1 - l_rate) * y_target[0][action] + l_rate * (
                        memory.reward + new_light_reward * gamma ** self.orange_phase_duration + max_next_action_value * gamma ** (
                        self.orange_phase_duration + 1))
            else:
                new_state_possible_actions_value_predictions = self.model.predict(memory.new_state.to_learn_array(self))
                max_next_action_value = max(new_state_possible_actions_value_predictions[
                                                0]) if memory.state.starting_actual_phase != 'orange' else \
                    new_state_possible_actions_value_predictions[0][-1]
                # print('maxcaxc',max_next_action_value)
                target = (1 - l_rate) * y_target[0][action] + l_rate * (
                        memory.reward + gamma * max_next_action_value)
            y_target[0][action] = target
            x_batch.append(state[0])
            y_batch.append(y_target[0])
        return x_batch, y_batch

    def last_epoch_batch(self):
        return self.memories[-90:]

    def reshape_rewards(self):
        max_time = Globals().vp().max_time_learn
        for i in range(len(self.memories)):  # - Globals().vp().reshape_future
            memory = self.memories[i]
            range_start_usable = i + (max_time - i % max_time) - Globals().not_to_learn_last_epochs
            range_end_usable = i + (max_time - i % max_time)
            # if i in range(max_time*(memory.epoch_index+1) - Globals().not_to_learn_last_epochs, max_time*(memory.epoch_index+1)):
            if range_start_usable < i < range_end_usable:
                memory.reshapedReward = True
                memory.learn_usable = False
            if not memory.reshapedReward:
                memory.reshapedReward = True
                furute_memories = [mem for mem in self.memories[i + 1:i + 1 + Globals().vp().reshape_future] if
                                   mem.epoch_index == memory.epoch_index]
                if len(furute_memories) < Globals().vp().reshape_future:
                    memory.learn_usable = False
                    continue
                memory.reward += sum([mem.reward for mem in furute_memories])
                self.memories[i] = memory

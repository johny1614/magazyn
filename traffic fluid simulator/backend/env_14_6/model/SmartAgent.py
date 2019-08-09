import matplotlib.pyplot as plt
import random
from statistics import mean
from typing import List
import attr
import numpy as np
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.python.keras import regularizers
from tensorflow.python.keras.callbacks import LambdaCallback
from tensorflow.python.keras.layers import Activation

from env_settings import max_time
from model.Agent import Agent
from model.Memory import Memory
from services.globals import Globals


@attr.s
class SmartAgent(Agent):
    memories: List[Memory] = attr.ib(factory=list)
    model = attr.ib(default=0)
    tensorboard = None
    weights_history = []

    def __attrs_post_init__(self):
        self.weights_history_callback = LambdaCallback(on_epoch_end=self.add_weight_history)
        if self.model == 0:
            l_rate = Globals().vp().nn_l_rate
            layers = Globals().vp().layers
            activation = 'relu'
            self.model = self._build_model(layers=layers, activation=activation, l_rate=l_rate)

    def _build_model(self, layers, activation='relu', l_rate=0.01, reg_val=Globals().vp().regularization):
        model = Sequential()
        for i, nodes in enumerate(layers):
            if i == 0:
                model.add(Dense(nodes, input_dim=6, activation='linear'))
            else:
                model.add(Dense(nodes, kernel_regularizer=regularizers.l2(reg_val)))
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

    def full_batch_no_orange(self, only_learn_usable=True):
        x_batch = []
        y_batch = []
        l_rate = Globals().learning_rate
        gamma = Globals().vp().gamma
        all_memories = self.memories
        # memories = self.memories if not only_learn_usable else [mem for mem in self.memories if mem.learn_usable]
        for i in range(len(all_memories)):
            memory=all_memories[i]
            if memory.action == 'orange' or not memory.learn_usable:
                continue
            state = memory.state.to_learn_array()
            action = memory.action
            y_target = self.model.predict(state)
            if not memory.holded_lights:
                if len(all_memories)<i+self.orange_phase_duration:
                    print('zle len')
                new_light_reward = all_memories[i+self.orange_phase_duration].reward
                # try:
                if(all_memories[i+self.orange_phase_duration].state.to_learn_array()[0][-1]=='orange'):
                    print(f'{i} starting_state={all_memories[i].state.starting_actual_phase} actual_state={all_memories[i].state.actual_phase} action={all_memories[i].action}')
                    print(f'{i+1} starting_state={all_memories[i+1].state.starting_actual_phase} actual_state={all_memories[i+1].state.actual_phase} action={all_memories[i+1].action}')
                    print(f'{i+2} starting_state={all_memories[i+2].state.starting_actual_phase} actual_state={all_memories[i+2].state.actual_phase} action={all_memories[i+2].action}')
                    print(f'{i+3} starting_state={all_memories[i+3].state.starting_actual_phase} actual_state={all_memories[i+3].state.actual_phase} action={all_memories[i+3].action}')
                    print(f'{i+4} starting_state={all_memories[i+4].state.starting_actual_phase} actual_state={all_memories[i+4].state.actual_phase} action={all_memories[i+4].action}')
                    print('zle')
                new_state_possible_actions_value_predictions = self.model.predict(all_memories[i+self.orange_phase_duration].state.to_learn_array())
                max_next_action_value=max(new_state_possible_actions_value_predictions[0])
                target = (1 - l_rate) * y_target[0][action] + l_rate * (
                        memory.reward + new_light_reward*gamma**self.orange_phase_duration+max_next_action_value*gamma**(self.orange_phase_duration+1) )
                # print('target',target)
                # except:
                #     a=34
                # print('state',state[0])
                # print('target',target)
            else:
                new_state_possible_actions_value_predictions = self.model.predict(memory.new_state.to_learn_array())
                max_next_action_value=max(new_state_possible_actions_value_predictions[0]) if memory.state.starting_actual_phase!='orange' else new_state_possible_actions_value_predictions[0][-1]
                # print('maxcaxc',max_next_action_value)
                target = (1 - l_rate) * y_target[0][action] + l_rate * (
                        memory.reward + gamma * max_next_action_value)
            y_target[0][action] = target
            x_batch.append(state[0])
            y_batch.append(y_target[0])
        return x_batch, y_batch

    def full_batch(self, only_learn_usable=False):
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
            max_next_action_value=max(new_state_possible_actions_value_predictions[0]) if memory.state.starting_actual_phase!='orange' else new_state_possible_actions_value_predictions[0][-1]
            target = (1 - l_rate) * y_target[0][action] + l_rate * (
                    memory.reward + gamma * max_next_action_value)
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

    def get_action(self, state,greedy=False):
        if state.actual_phase == 'orange':
            return 'orange'
        if np.random.rand() <= Globals().epsilon and not greedy:  # if acting randomly, take random action
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
            range_start_usable = i + (max_time-i%max_time) - Globals().not_to_learn_last_epochs
            range_end_usable = i + (max_time-i%max_time)
            # if i in range(max_time*(memory.epoch_index+1) - Globals().not_to_learn_last_epochs, max_time*(memory.epoch_index+1)):
            if range_start_usable < i <range_end_usable:
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
                # print('rew',memory.reward)
                # if 3 < memory.state.densities[0] < 5 and 9 < memory.state.densities[
                #     1] < 15 and memory.action == 1 and memory.state.starting_actual_phase == 1:
                #     print(f'state {memory.state.densities[0]},{memory.state.densities[1]} a:{memory.action}')
                #     print('reww', memory.reward)
                #     rew powinno byc przynajmniej 9!
                # else:
                #     print(f'state {memory.state.densities[0]},{memory.state.densities[1]} a:{memory.action}')

    def add_weight_history(self, epoch, logs):
        self.weights_history.append(self.model.get_weights())
        # if epoch %

    def plot_weights(self):
        # print('done',Globals().epochs_done)
        if len(self.weights_history)==0:
            return
        layers = range(len(self.weights_history[0]) - 1)
        bias_layers = []
        a_layers = []
        for layer in layers:
            if len(self.weights_history[0][layer].shape) == 2:
                a_layers.append(layer)
            if len(self.weights_history[0][layer].shape) == 1:
                bias_layers.append(layer)
        for bias_layer in bias_layers:
            neurons = range(len(self.weights_history[0][bias_layer]))
            for n in neurons:
                color = [1 - n / len(neurons), n / len(neurons), 0]
                plt.plot([x[bias_layer][n] for x in self.weights_history], color=color, label=str(n))
            name = 'weights_layer_' + str(bias_layer) + '.png'
            plt.savefig(name)
            plt.close()
        node = 0
        for a_layer in a_layers:
            draw = 0
            previous_nodes = range(len(self.weights_history[0][a_layer]))
            layer_nodes = range(len(self.weights_history[0][a_layer][0]))
            all_weights = len(previous_nodes) * len(layer_nodes)
            max_nodes = 15
            for prev_node in previous_nodes:
                for layer_node in layer_nodes:
                    color = [1 - node / max_nodes, node / max_nodes, 0]
                    plt.plot([x[a_layer][prev_node][layer_node] for x in self.weights_history], color=color,
                             label=str(n))
                    node += 1
                    if node > max_nodes:
                        node = 0
                        # print('node',node)
                        # print('draw',draw)
                        name = 'weights_layer_' + str(a_layer) + '_draw_' + str(draw) + '.png'
                        plt.savefig(name)
                        plt.close()
                        draw += 1
            name = 'weights_layer_' + str(a_layer) + '_draw_' + str(draw) + '.png'
            plt.savefig(name)
            plt.close()

        # if Globals().epochs_done > 5:
        #     layers = range(len(self.weights_history[0]) - 1)
        #     for layer in layers:
        #         neurons = range(len(self.weights_history[0][layer]))
        #         max_lines = 15.0
        #         draw = 0
        #         line_index=0
        #         for n in neurons:
        #             color = [1 - line_index / max_lines, line_index / max_lines, 0]
        #             plt.plot([x[layer][n] for x in self.weights_history], color=color, label=str(n))
        #             name = 'weights_layer_' + str(layer) + 'draw' + str(draw)+'.png'
        #             line_index += 1
        #             if line_index >= max_lines:
        #                 draw += 1
        #                 line_index=0
        #                 try:
        #                     plt.savefig(name)
        #                     plt.close()
        #                 except:
        #                     print('nie matakiego otwierania!')
        #         plt.savefig(name)
        #         plt.close()

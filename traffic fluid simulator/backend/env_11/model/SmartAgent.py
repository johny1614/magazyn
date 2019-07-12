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
from model.Agent import Agent
from model.Memory import Memory
from services.globals import Globals


@attr.s
class SmartAgent(Agent):
    memories: List[Memory] = attr.ib(factory=list)
    Q = {}
    Returns = {}
    Pi = {}

    # def __attrs_post_init__(self):
    #     # INIT PI and Q
    #     densitiesPossible = [x * 0.1 for x in range(100)]
    #     phases = [0, 1, 'orange']
    #     actions = [0, 1, 'orange']
    #     for firstDen in densitiesPossible:
    #         for secondDen in densitiesPossible:
    #             for phase in phases:
    #                 tpl = (firstDen, secondDen, phase)
    #                 self.Pi[tpl] = random.choice(actions)
    #                 for action in actions:
    #                     self.Q[tpl, action] = 0

    def get_action(self, state):
        if state.to_learn_tuple_used()[-1] == 'orange' and Globals().time!=0:
            return 'orange'
        s = state.to_learn_tuple_used()
        if random.random() < Globals().epsilon:
            random_action = random.choice([0, 1])
            return random_action
        if s not in self.Pi:
            self.Pi[s] = random.choice([0, 1])
            # print(f'time {Globals().time} wylosowane a: {self.Pi[s]}')
        # else:
        #     print(f'time {Globals().time} mamy a: {self.Pi[s]}')
        return self.Pi[s]

    def save_batch(self):
        x_batch = []
        y_batch = []
        for memory in self.memories:
            if memory.action == 'orange':
                continue
            state = memory.state.to_learn_tuple_used()
            y = memory.reward
            x_batch.append(state[0])
            y_batch.append(y)
            if self.index == 0:
                Globals().x_batch.append(state[0])
                Globals().y_batch.append(y)

    def count_G(self):
        last_memories = self.last_epoch_batch()
        indexes = range(len(last_memories)).__reversed__()
        for i in indexes:
            if i == len(last_memories) - 1:
                G = last_memories[i].reward
            else:
                G = last_memories[i].reward + last_memories[i + 1].reward * Globals().gamma
            s = last_memories[i].state.to_learn_tuple_used()
            a = last_memories[i].action
            if s in self.Returns:
                self.Returns[s, a].append(G)
            else:
                self.Returns[s, a] = [G]

    def count_Q(self):
        last_memories = self.last_epoch_batch()
        for mem in last_memories:
            s = mem.state.to_learn_tuple_used()
            a = mem.action
            self.Q[s, a] = mean(self.Returns[s, a])

    def count_PI(self):
        last_memories = self.last_epoch_batch()
        for mem in last_memories:
            s = mem.state.to_learn_tuple_used()
            a = mem.action
            # TODO argmaxem sie nie da  - akcje dla ktorej jest najwyzsza wartosc z mean returns przy danym s
            if random.random() < Globals().epsilon:
                random_action = random.choice([0, 1]) if a in [0, 1] else "orange"
                self.Pi[s, a] = random_action
            actions = [0, 1, 'orange']
            best_value = -1000
            best_action = 0
            for action in actions:
                if (s, action) not in self.Returns:
                    continue
                actual_value = mean(self.Returns[s, action])
                if actual_value > best_value:
                    best_action = action
                    best_value = actual_value
                # if (s,a) in self.Pi and best_action!=a:
                #     print('jest zmieniona strategia!!!!!!')
            self.Pi[s, a] = best_action

    def remember(self, densities, reward):
        state = self.local_state
        action = self.action
        self.assign_local_state(densities)
        new_state = self.local_state
        times = {'old': Globals().time - 1, 'new': Globals().time}
        memory = Memory(state=state, action=action, new_state=new_state, reward=reward, times=times)
        self.memories.append(memory)

    def last_epoch_batch(self):
        return self.memories[-90:]

    def reshape_rewards(self):
        for i in range(len(self.memories) - 3):
            memory = self.memories[i]
            if not memory.reshapedReward:
                memory.reshapedReward = True
                future_rewards = [mem.reward for mem in self.memories[i + 1:i + 3]]  # 2 next rewards
                memory.reward += sum(future_rewards)
                self.memories[i] = memory

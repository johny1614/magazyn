from typing import Tuple, Dict, List
import attr
import numpy as np

from Env import Env
from env_data import sections_of_roads
from model.Action import Action
from model.Agent import Agent
from model.LearningState import LearningState
import random

from services.densityGroups import getGroup
from services.globals import Globals


def empty_dic():
    return {}


@attr.s(auto_attribs=True)
class SmartAgent(Agent):
    returns: Dict[Tuple[LearningState, Action], List[float]] = attr.ib(default=attr.Factory((empty_dic)))
    Q: Dict[LearningState, Action] = attr.ib(default=attr.Factory((empty_dic)))
    pi: Dict[LearningState, Action] = attr.ib(default=attr.Factory((empty_dic)))

    def get_action_according_to_pi(self, learning_state: LearningState,random_probabilty: float) -> Action:
        if(random_probabilty):
            rand_value=random.random()
            if(rand_value<random_probabilty):
                return random.choice(list(self.local_action_space))
        if learning_state not in self.pi:
            # print('adding leagning state',learning_state)
            random_action = random.choice(list(self.local_action_space))
            self.pi[learning_state] = random_action
        # else:
        if self.pi[learning_state] not in self.local_action_space:
            return random.choice(list(self.local_action_space))
        return self.pi[learning_state]

    def add_returns(self, G):
        for i in range(len(G)):
            if ((self.epoch_local_state_storage[i], self.epoch_local_action_storage[i]) in self.returns.keys()):
                self.returns[self.epoch_local_state_storage[i], self.epoch_local_action_storage[i]].append(G[i])
                Globals().state_repeats += 1
            else:
                Globals().new_states += 1
                self.returns[self.epoch_local_state_storage[i], self.epoch_local_action_storage[i]] = [G[i]]
        print('powtorki',Globals().state_repeats)
        print('nowe',Globals().new_states)
    def update_Q(self):
        for i in range(len(self.epoch_local_state_storage)):
            state = self.epoch_local_state_storage[i]
            action = self.epoch_local_action_storage[i]
            self.Q[state, action] = np.mean(self.returns[state, action])

    def update_pi(self):
        for i in range(len(self.epoch_local_state_storage) - 1):
            state = self.epoch_local_state_storage[i]
            self.pi[state] = self.find_best_Q(state)

    def clear_epoch_local_data(self):
        self.epoch_local_state_storage = ()
        self.epoch_local_action_storage = ()

    def find_best_Q(self, state):
        bestValue = -9
        bestAction = None
        keys_of_state = [key for key in self.Q.keys() if key[0] == state]
        for key in self.Q.keys():
            if (self.Q[key] >= bestValue):
                bestValue == self.Q[key]
                bestAction = key[1]
        return bestAction
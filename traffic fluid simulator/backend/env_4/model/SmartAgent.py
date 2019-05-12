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


def empty_dic():
    return {}


@attr.s(auto_attribs=True)
class SmartAgent(Agent):
    returns: Dict[Tuple[LearningState, Action], float] = attr.ib(default=attr.Factory((empty_dic)))
    Q: Dict[LearningState, Action] = attr.ib(default=attr.Factory((empty_dic)))
    pi: Dict[LearningState, Action] = attr.ib(default=attr.Factory((empty_dic)))
    # epoch_states_rewards: Dict[LearningState] = attr.ib(default=attr.Factory((empty_dic)))

    def get_action_according_to_pi(self, learning_state: LearningState) -> Action:
        if learning_state not in self.pi:
            random_action = random.choice(list(self.local_action_space))
            self.pi[learning_state] = random_action
        return self.pi[learning_state]

    def pass_returns(self, env: Env):
        print('env', env)

        # self.epoch_states_rewards.append(local_state)

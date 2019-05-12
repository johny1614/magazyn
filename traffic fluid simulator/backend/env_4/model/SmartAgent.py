from typing import Tuple, Dict
import attr
from model.Action import Action
from model.Agent import Agent
from model.LearningState import LearningState
import random


def empty_dic():
    return {}


@attr.s(auto_attribs=True)
class SmartAgent(Agent):
    returns: Dict[Tuple[LearningState, Action], float] = attr.ib(default=attr.Factory((empty_dic)))
    Q: Dict[LearningState, Action] = attr.ib(default=attr.Factory((empty_dic)))
    pi: Dict[LearningState, Action] = attr.ib(default=attr.Factory((empty_dic)))

    def get_action_according_to_pi(self, learning_state: LearningState) -> Action:
        if learning_state not in self.pi:
            random_action = random.choice(list(self.local_action_space))
            self.pi[learning_state] = random_action
        return self.pi[learning_state]

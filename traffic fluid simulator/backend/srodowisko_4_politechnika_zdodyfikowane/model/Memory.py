from typing import List

import attr

from model.Action import ActionInt
from model.LearningState import LearningState


@attr.s(auto_attribs=True)
class Memory:
    state: LearningState
    action: ActionInt
    reward: any  # float, ale to psuje
    new_state: LearningState
    times: any
    epoch_index: int
    learn_usable: bool = True
    reshapedReward: bool = False
    holded_lights = None

    def __attrs_post_init__(self):
        self.holded_lights = self.action == self.state.starting_actual_phase

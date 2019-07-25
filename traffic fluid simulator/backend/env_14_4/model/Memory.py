
import attr

from model.Action import ActionInt
from model.LearningState import LearningState


@attr.s(auto_attribs=True)
class Memory:
    state: LearningState
    action: ActionInt
    reward: any # float, ale to psuje
    new_state: LearningState
    times: any
    epoch_index: int
    learn_usable: bool = True
    reshapedReward: bool = False

import attr

from model.Action import ActionInt
from model.LearningState import LearningState


@attr.s(auto_attribs=True)
class Memory:
    state: LearningState
    action: ActionInt
    reward: any  # float, ale to psuje obliczenia
    new_state: LearningState
    times: any
    reshapedReward: bool = False

from typing import List
from Env import Env
from model.Action import yellow, ActionInt
from services.globals import Globals


def epoch_greedy(env) -> Env:
    Globals().time = 0
    actions_count_0 = [0, 0, 0, 0, 0]
    actions_count_1 = [0, 0, 0, 0, 0]
    actions_count_2 = [0, 0, 0, 0, 0]
    actions_count_3 = [0, 0, 0, 0, 0]
    for t in range(Globals().vp.max_time_greedy):
        actions: List[ActionInt] = [agent.get_action(state=agent.local_state, greedy=True) for agent in env.agents]
        env.step(actions)
        if actions[0] != yellow:
            actions_count_0[int(actions[0])] += 1
        else:
            actions_count_0[-1] += 1
        if actions[1] != yellow:
            actions_count_1[int(actions[1])] += 1
        else:
            actions_count_1[-1] += 1
        if actions[2] != yellow:
            actions_count_2[int(actions[2])] += 1
        else:
            actions_count_2[-1] += 1
        if actions[3] != yellow:
            actions_count_3[int(actions[3])] += 1
        else:
            actions_count_3[-1] += 1
    return env.u
    print('akcje podjete', [actions_count_0, actions_count_1, actions_count_2, actions_count_3])

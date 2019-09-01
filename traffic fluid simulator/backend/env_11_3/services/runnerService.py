from typing import List
from Env import Env
from env_settings import max_time
from model.Action import ActionInt
from services.globals import Globals


def epoch_greedy(env) -> Env:
    Globals().time = 0
    Globals().epsilon = 0
    actions_count = [0, 0]
    for t in range(max_time):
        actions: List[ActionInt] = [agent.get_action(agent.local_state) for agent in env.agents]
        actions_count[actions[0]] += 1
        env.step(actions)
    print(actions_count)
    return env

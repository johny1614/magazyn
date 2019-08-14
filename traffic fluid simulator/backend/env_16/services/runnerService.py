import random
from typing import List

from Env import Env
from model.SmartAgent import SmartAgent
from services.agentFactory import get_SmartAgents
from services.globals import Globals

ActionInt = int


def epoch_sequence(env, actions_function,max_time) -> Env:
    Globals().time = 0
    for t in range(max_time):
        actions: List[ActionInt] = actions_function(t)
        env.step(actions)
    return env


def epoch_random(env) -> Env:
    Globals().epsilon = 0
    agents: List[SmartAgent] = get_SmartAgents()
    for t in range(Globals().vp().max_time_learn):
        actions: List[ActionInt] = [random.choice(agent.local_action_space) for agent in agents]
        env.step(actions)
    return Env


def epoch_greedy(env) -> Env:
    Globals().time = 0
    for t in range(Globals().vp().max_time_greedy):
        # print('state',env.agents[0].local_state)
        actions: List[ActionInt] = [agent.get_action(state=agent.local_state,greedy=True) for agent in env.agents]
        env.step(actions)
 
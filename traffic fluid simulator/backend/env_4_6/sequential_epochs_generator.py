import os

import numpy as np

import env_settings
from runner import epoch_sequence

os.environ["PATH"] += os.pathsep + 'C:/Graphviz/bin'
from typing import List
from Env import Env
from env_settings import max_time
from model.SmartAgent import SmartAgent
from services.agentFactory import get_SmartAgents
from services.globals import Globals

ActionInt = int


def actions_fun(t):
    actions = [1, 1, 1]
    if t == 60 or t >= 62:
        actions = [2, 2, 2]
    if t == 61:
        actions = [0, 0, 0]
    return actions


agents: List[SmartAgent] = get_SmartAgents()
env = Env(agents)
epochs = range(1)
for e in epochs:
    Globals().epsilon = 1
    env: Env = epoch_sequence(env, actions_fun)
    for agent in env.agents:
        agent.reshape_rewards()

env.update_global_memory_rewards()
# for agent in agents:
#     agent.save_batch()
agents[0].save_batch()
np.savetxt('static_files/x_batch.txt', Globals().x_batch, delimiter=',')
np.savetxt('static_files/y_batch.txt', Globals().y_batch, delimiter=',')

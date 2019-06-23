import os

import numpy as np

import env_settings
from model.ExportData import ExportData
from runner import epoch_sequence

os.environ["PATH"] += os.pathsep + 'C:/Graphviz/bin'
from typing import List
from Env import Env
from env_settings import max_time
from model.SmartAgent import SmartAgent
from services.agentFactory import get_SmartAgents
from services.globals import Globals

ActionInt = int
orange = 'orange'


def actions_fun(t):
    actions = [1, 1, 1]
    if t == 60 or t >= 63:
        actions = [1, 1, 1]
    if t == 61 or t == 62:
        actions = [orange, orange, orange]
    return actions


agents: List[SmartAgent] = get_SmartAgents()
env = Env(agents)
epochs = range(1)
for e in epochs:
    Globals().epsilon = 1
    env: Env = epoch_sequence(env, actions_fun)
    for agent in env.agents:
        agent.reshape_rewards()

# for agent in agents:
#     agent.save_batch()
# env.update_global_memory_rewards()
exportData = ExportData(learningMethod='Monte Carlo TODO', learningEpochs=0, nets=env.global_memories,
                                netName='net4',
                                densityName='seq')
exportData.saveToJson()
print('a')
# agents[0].save_batch()
# np.savetxt('static_files/x_batch.txt', Globals().x_batch, delimiter=',')
# np.savetxt('static_files/y_batch.txt', Globals().y_batch, delimiter=',')

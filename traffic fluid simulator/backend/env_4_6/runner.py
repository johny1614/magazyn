import matplotlib.pyplot as plt
# 2 odcinki na droge!
import os
import random

import numpy as np

os.environ["PATH"] += os.pathsep + 'C:/Graphviz/bin'
from typing import List
from matplotlib import pyplot
from Env import Env
from Utils import nested_sum
from env_settings import max_time
from model.ExportData import ExportData
from model.Net import Net
from model.SmartAgent import SmartAgent
from services.agentFactory import get_SmartAgents, get_LearnSmartAgents
from services.globals import Globals
from services.parser import get_G

ActionInt = int


def getActions(t):
    actions = [1, 1, 1]
    if t == 60 or 63 <= t < 70:
        actions = [2, 2, 2]
    if t == 61 or t == 62:
        actions = [0, 0, 0]
    if t == 70 or t >= 73:
        actions = [3, 3, 3]
    if t == 71 or t == 72:
        actions = [0, 0, 0]
    return actions


def epoch(actions_function):
    Globals().time = 0
    env = Env(agents)
    for t in range(max_time):
        actions: List[ActionInt] = actions_function(t)
        # actions = best_actions[t] if len(best_actions)>=t else [0,0,0]
        env.step(actions)
    Globals().epochs_done += 1
    return env


Globals().max_epsilon = 0
agents: List[SmartAgent] = get_SmartAgents()
epochs = range(1)
for e in epochs:
    env: Env = epoch(getActions)  # :1
#     rewards = nested_sum(env.global_rewards)
# print('rewards', rewards)
# print('carsout', env.cars_out)

env.agents[0].reshape_rewards()
env.update_global_memory_rewards()
env.agents[0].save_batch()
exportData = ExportData(learningMethod='Monte Carlo TODO', learningEpochs=0, nets=env.global_memories, netName='net4',
                        densityName='sequential')
exportData.saveToJson()
np.savetxt('x_batch.txt', Globals().x_batch, delimiter=',')
np.savetxt('y_batch.txt', Globals().y_batch, delimiter=',')

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
from env_data import max_time
from model.ExportData import ExportData
from model.Net import Net
from model.SmartAgent import SmartAgent
from services.agentFactory import get_SmartAgents, get_LearnSmartAgents
from services.globals import Globals
from services.parser import get_G

ActionInt = int


def epoch():
    Globals().time = 0
    env = Env(agents)
    for t in range(max_time):
        actions: List[ActionInt] = [agent.get_action(agent.local_state) for agent in agents]
        env.step(actions)
    Globals().epochs_done += 1
    return env


Globals().max_epsilon=0
agents: List[SmartAgent] = get_LearnSmartAgents()
env: Env = epoch()  # :1
rewards = nested_sum(env.global_rewards)
print('rewards', rewards)
print('carsout', env.cars_out)

exportData = ExportData(learningMethod='Monte Carlo TODO', learningEpochs=0, nets=env.global_memories, netName='net4',
                        densityName='last_epoch')
exportData.saveToJson()

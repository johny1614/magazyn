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


def epoch(agents):
    Globals().time = 0
    env = Env(agents)
    for t in range(max_time):
        actions: List[ActionInt] = [random.choice(agent.local_action_space) for agent in agents]
        env.step(actions)
    Globals().epochs_done += 1
    return env


def run_random(epochs, agents=None) -> List[SmartAgent]:
    Globals().max_epsilon = 0
    if agents == None:
        agents: List[SmartAgent] = get_SmartAgents()
    for e in epochs:
        env: Env = epoch(agents)
    return agents

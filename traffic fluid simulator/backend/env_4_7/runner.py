# 2 odcinki na droge!
import os
import random

os.environ["PATH"] += os.pathsep + 'C:/Graphviz/bin'
from typing import List
from Env import Env
from env_settings import max_time
from model.SmartAgent import SmartAgent
from services.agentFactory import get_SmartAgents
from services.globals import Globals

ActionInt = int

def getActions(t): # example of function to epoch_sequence
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


def epoch_sequence(env,actions_function):
    Globals().time = 0
    for t in range(max_time):
        actions: List[ActionInt] = actions_function(t)
        env.step(actions)
    return env


def epoch_random(env):
    Globals().epsilon = 0
    agents: List[SmartAgent] = get_SmartAgents()
    for t in range(max_time):
        actions: List[ActionInt] = [random.choice(agent.local_action_space) for agent in agents]
        env.step(actions)
    return agents




def epoch_greedy(env):
    Globals().time = 0
    Globals().epsilon = 0
    for t in range(max_time):
        actions: List[ActionInt] = [agent.get_action(agent.local_state) for agent in env.agents]
        env.step(actions)
    return env
# Wazne rzeczy!
# env.agents[0].reshape_rewards()
# env.update_global_memory_rewards()
# env.agents[0].save_batch()
# exportData = ExportData(learningMethod='Monte Carlo TODO', learningEpochs=0, nets=env.global_memories, netName='net4',
#                         densityName='sequential')
# exportData.saveToJson()
# np.savetxt('x_batch.txt', Globals().x_batch, delimiter=',')
# np.savetxt('y_batch.txt', Globals().y_batch, delimiter=',')

import os

import numpy as np

import env_settings
from model.ExportData import ExportData

os.environ["PATH"] += os.pathsep + 'C:/Graphviz/bin'
from typing import List
from Env import Env
from env_settings import max_time
from model.SmartAgent import SmartAgent
from services.agentFactory import get_SmartAgents
from services.globals import Globals

ActionInt = int


def epoch(agents, u=env_settings.u_all_2):
    Globals().time = 0
    env = Env(agents)
    env.u = u
    for t in range(max_time):
        actions: List[ActionInt] = [agent.get_action(agent.local_state) for agent in agents]
        env.step(actions)
    Globals().epochs_done += 1
    return env

epochs = range(100)
# epochs = range(1, 2)
xy_20_all = []
agents: List[SmartAgent] = get_SmartAgents()
for e in epochs:
    Globals().epsilon = 1
    env: Env = epoch(agents,u=env_settings.u_all_4)
    for agent in env.agents:
        agent.reshape_rewards()
    env.update_memory_rewards()
    env.remember_memory()
    # exportData = ExportData(learningMethod='DQN', learningEpochs=0, nets=env.global_memories,
    #                         netName='net4',
    #                         densityName='random_' + str(e))
    # exportData.saveToJson()
    x_batch, y_batch = agents[0].memory_to_minibatch_with_oranges()
    xy_20 = [(x_batch[i], y_batch[i], i, agents[0].memories[i], e) for i in range(len(x_batch)) if
             25 > x_batch[i][2] > 15 and agents[0].memories[i].action == 0]
    if len(xy_20) > 0:
        xy_20_all.append(xy_20)
    # i = 2

for i in range(len(agents)):
    print(i)
    filename = 'static_files/x_batch_agent_' + str(i) + '.txt'
    x_batch, y_batch = agents[i].full_batch()
    np.savetxt(filename, x_batch, delimiter=',')
    filename = 'static_files/y_batch_agent_' + str(i) + '.txt'
    np.savetxt(filename, y_batch, delimiter=',')
    # filename = 'static_files/y_batch_agent_batch_time' + str(i) + '.txt'
    # np.savetxt(filename, (x_batch, y_batch), delimiter=',')
full_batch=agents[0].full_batch()
orange_batch = agents[0].memory_to_minibatch_with_oranges()
a = 2
# env.update_global_memory_rewards()
# x_batch, y_batch = agents[0].full_batch()
# np.savetxt('static_files/x_batch_agent_0.txt',Globals().x_batch,delimiter=',')
# np.savetxt('static_files/y_batch_agent_0.txt',Globals().y_batch,delimiter=',')

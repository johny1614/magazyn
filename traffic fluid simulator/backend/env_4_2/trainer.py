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
from services.agentFactory import get_SmartAgents
from services.globals import Globals
from services.parser import get_G

ActionInt = int


def ez_stategy():
    if t > 1:
        actions = []
        for agent in env.agents:
            best_action = -2
            best_action_value = -20
            for i in range(len(agent.local_phase_sections)):
                section = agent.local_phase_sections[i]
                action_value = env.x[t - 1][section]
                # print('a value', action_value)
                if action_value > best_action_value:
                    best_action_value = action_value
                    for action_index in range(len(agent.moves)):
                        moves = agent.moves[action_index]
                        for move in moves:
                            if move[1] == section:
                                best_action = action_index
            # print(f'akcja{best_action} value:{best_action_value}')
            actions.append(best_action)
    # print(f'{t}:{actions}')


def epoch():
    Globals().time = 0
    env = Env(agents)
    for t in range(max_time):
        actions: List[ActionInt] = [agent.get_action(agent.local_state) for agent in agents]
        # print(actions)
        # actions: List[ActionInt] = [3,3,3]
        # if t >= 30:
        #     actions = [2,2,3]
        # if t==31:
        # print('31 kurwa!')
        # print(f'time:{t}')
        env.step(actions)
        # print('x', env.x[t])
    Globals().epochs_done += 1
    return env


agents: List[SmartAgent] = get_SmartAgents()
best_score = 0
scores = []
epochs = range(2000)
our_memories = None
last_epoch = None
global_rewards = []
best_reward = -100
session_rewards = []
for e in epochs:
    # print('============================',e)
    env: Env = epoch()  # :1
    # print(env.cars_out)
    rewards = nested_sum(env.global_rewards)
    global_rewards.append(rewards)
    if rewards > best_reward:
        best_reward = rewards
        our_memories = env.global_memories
        best_score = env.cars_out
        our_env = env
    session_rewards.append(rewards)
    scores.append(env.cars_out)
    # print(f'Epizod:{e} Cars_out:{round(env.cars_out)} reward:{round(rewards)} epsilon:{Globals().epsilon()}')
    # pred = env.agents[0].model.predict(np.array([[7, 1, 1,1]]))
    # print(pred)
    if env.cars_out > best_score:
        best_score = env.cars_out
        our_memories = env.global_memories
    # if i%10==0:
    exportData = ExportData(learningMethod='Monte Carlo TODO', learningEpochs=0, nets=our_memories, netName='net4',
                            densityName='cross')
    exportData.saveToJson()
    for agent in env.agents:
        agent.train()
    pred = env.agents[0].model.predict(np.array([[1,7,1,2]]))
    print(pred)
    env.agents[0].model.evaluate(np.array(Globals().x_batch), np.array(Globals().y_batch))
    if e == epochs[-1]:
        last_epoch = env.global_memories
print('srednia rewardow', sum(session_rewards) / len(session_rewards))
pyplot.plot(global_rewards)
pyplot.show()

print('score to', best_score)

for agent in env.agents:
    name = 'agent' + str(agent.index) + '.h5'
    agent.model.save(name)

exportData = ExportData(learningMethod='Monte Carlo TODO', learningEpochs=0, nets=our_memories, netName='net4',
                        densityName='77')
exportData.saveToJson()
exportData = ExportData(learningMethod='Monte Carlo TODO', learningEpochs=0, nets=our_memories, netName='net4',
                        densityName='last_epoch')
exportData.saveToJson()
pass

# np.savetxt('x_batch.txt',Globals().x_batch,delimiter=',')
# np.savetxt('y_batch.txt',Globals().y_batch,delimiter=',')

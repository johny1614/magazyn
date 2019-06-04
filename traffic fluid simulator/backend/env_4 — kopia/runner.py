import matplotlib.pyplot as plt
# 2 odcinki na droge!

from typing import List
from matplotlib import pyplot
from Env import Env
from env_data import max_time
from model.ExportData import ExportData
from model.Net import Net
from model.SmartAgent import SmartAgent
from services.agentFactory import get_SmartAgents
from services.globals import Globals
from services.parser import get_G

ActionInt=int

def epoch():
    Globals().time = 0
    env = Env(agents)
    for t in range(max_time):
        actions: List[ActionInt] = [agent.get_action(agent.local_state) for agent in agents]
        actions=[1,1,1]
        env.step(actions)
    Globals().epochs_done+=1
    return env

agents: List[SmartAgent] = get_SmartAgents()
best_score = 0
scores=[]
epochs = range(5)
our_memories = None
global_rewards=[]
best_reward=-100
for e in epochs:
    env: Env = epoch()  # :1
    # print(env.cars_out)
    rewards = sum(env.global_rewards)
    global_rewards.append(rewards)
    if rewards > best_reward:
        best_reward = rewards
        our_memories = env.global_memories
        best_score = env.cars_out
    # global_rewards.append(sum(env.global_rewards))
    # scores.append(env.cars_out)
    print(env.cars_out)
    # if env.cars_out > best_score:
    #     best_score=env.cars_out
    #     our_memories = env.global_memories
    for agent in env.agents:
        agent.train()
# for memory in env.global_memories:
    # nets.append({'densities': m['state'], 'lights': m['action']})
# data = {
#     'nets': env.global_memories,
#     'rewards sum': 70,
#     'gamma': gamma,
#     'learningEpochs': len(epochs),
#     'learningMethod': 'Monte Carlo',
#     # 'turns':env.turns
# }
# #
pyplot.plot(global_rewards)
pyplot.show()

print('score to',best_score)

exportData = ExportData(learningMethod='Monte Carlo TODO', learningEpochs=0, nets=our_memories, netName='net4',
                        densityName='77')
exportData.saveToJson()

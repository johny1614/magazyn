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
        env.step(actions)
    return env

agents: List[SmartAgent] = get_SmartAgents()
gamma = 0.8
epsilon = 0.2
best_score = 0
scores=[]
epochs = range(450)
our_memories = None
for e in epochs:
    env: Env = epoch()  # :1
    print(env.cars_out)
    scores.append(env.cars_out)
    if env.cars_out > best_score:
        best_score=env.cars_out
        our_memories = env.global_memories
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
pyplot.plot(scores)
pyplot.show()


exportData = ExportData(learningMethod='Monte Carlo TODO', learningEpochs=0, nets=our_memories, netName='net4',
                        densityName='77')
exportData.saveToJson()

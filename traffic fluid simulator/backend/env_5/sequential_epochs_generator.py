import os

from model.ExportData import ExportData
from services.runnerService import epoch_sequence
import matplotlib.pyplot as plt

os.environ["PATH"] += os.pathsep + 'C:/Graphviz/bin'
from typing import List
from Env import Env
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

cars_outs=[]
rewards=[]
rewards_mean=[]
agents: List[SmartAgent] = get_SmartAgents()
env = Env(agents)
epochs = range(40)
for e in epochs:
    Globals().epsilon = 1
    env: Env = epoch_sequence(env, actions_fun)
    for agent in env.agents:
        agent.reshape_rewards()
    cars_outs.append(env.cars_out)
    rewards.append(env.count_rewards()[0])
    rewards_mean.append(env.count_rewards()[1])

# for agent in agents:
#     agent.save_batch()
# env.update_global_memory_rewards()
exportData = ExportData(learningMethod='Monte Carlo TODO', learningEpochs=0, nets=env.global_memories,
                                netName='net4',
                                densityName='seq')
exportData.saveToJson()
plt.plot(cars_outs)
plt.title='cars_out random'
plt.savefig('img_cars_out_random.png')
plt.close()
plt.plot(rewards_mean)
plt.title='rewards mean random'
plt.savefig('img_rewards_mean_random.png')
plt.close()
plt.plot(rewards)
plt.title='rewards random'
plt.savefig('img_rewards_random.png')
plt.close()

# agents[0].save_batch()
# np.savetxt('static_files/x_batch.txt', Globals().x_batch, delimiter=',')
# np.savetxt('static_files/y_batch.txt', Globals().y_batch, delimiter=',')

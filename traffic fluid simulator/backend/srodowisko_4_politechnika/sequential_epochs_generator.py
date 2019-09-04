import os

from env_settings import u_all_2, u_v1, u
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
    actions = [1]
    if t == 60 or t >= 63:
        actions = [1]
    if t == 61 or t == 62 or t == 1 or t == 2:
        actions = [orange]
    return actions


def actions_fun2(t):
    actions = [1]
    if t == 0:
        actions = [0]
    if t == 20 or t >= 23:
        actions = [1]
    if t == 21 or t == 22 or t == 1 or t == 2:
        actions = [orange]
    return actions


cars_outs = []
rewards = []
rewards_mean = []
agents: List[SmartAgent] = get_SmartAgents()
env = Env(agents)
# env.u = u_all_2
env.u = u
epochs = range(1)
for e in epochs:
    Globals().epsilon = 1
    env: Env = epoch_sequence(env, actions_fun)
    for agent in env.agents:
        agent.reshape_rewards()
    cars_outs.append(env.cars_out)
    rewards.append(env.count_rewards()[0])
    rewards_mean.append(env.count_rewards()[0])
# env = Env(agents)
# for e in epochs:
#     Globals().epsilon = 1
#     env: Env = epoch_sequence(env, actions_fun2)
#     for agent in env.agents:
#         agent.reshape_rewards()
#     cars_outs.append(env.cars_out)
#     rewards.append(env.count_rewards()[0])
#     rewards_mean.append(env.count_rewards()[0])

# for agent in agents:
#     agent.save_batch()
# env.update_global_memory_rewards()
exportData = ExportData(learningMethod='Monte Carlo TODO', learningEpochs=0, nets=env.global_memories,
                        netName='net11',
                        densityName='seq')
print(env.cars_out)
exportData.saveToJson()
# plt.plot(cars_outs)
# plt.title = 'cars_out random'
# plt.savefig('img_cars_out_random.png')
# plt.close()
# plt.plot(rewards_mean)
# plt.title = 'rewards mean random'
# plt.savefig('img_rewards_mean_random.png')
# plt.close()
# plt.plot(rewards)
# plt.title = 'rewards random'
# plt.savefig('img_rewards_random.png')
# plt.close()

# agents[0].save_batch()
# np.savetxt('static_files/x_batch.txt', Globals().x_batch, delimiter=',')
# np.savetxt('static_files/y_batch.txt', Globals().y_batch, delimiter=',')

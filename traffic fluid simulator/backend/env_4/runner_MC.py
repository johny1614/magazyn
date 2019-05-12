# 2 odcinki na droge!

from typing import List

from Env import Env
from env_data import max_time
from model.Action import Action
from model.ExportData import ExportData
from model.Net import Net
from model.SmartAgent import SmartAgent
from services.agentFactory import get_SmartAgents
from services.globals import Globals


def epoch():
    Globals().time = 0
    env = Env(agents)
    for t in range(max_time):
        actions: List[Action] = [agent.get_action_according_to_pi(agent.local_state) for agent in agents]
        env.step(actions)
    return env
    #     state = local_states
    #     memories.append({'state': old_state, 'new_state': state, 'action': actions, 'reward': reward})
    # return memories


agents: List[SmartAgent] = get_SmartAgents()
gamma = 1
epsilon = 0.2
# state_space = []  # poczotkowo nic [(x, y, z) for x in range(52) for y in range(52) for z in range(52)]
best_score = 0
epochs = range(1)
for e in epochs:
    env: Env = epoch()
    nets: List[Net] = []
    for t in range(max_time - 1):
        A = env.A_storage[t + 1].tolist()
        x = env.x[t].tolist()
        nets.append(Net(A, x))
print('end')
#     epoch_rewards = count_rewards(epoch_memory)
# last_epoch_memory = epoch()  # last epoch
# reward_sum = count_rewards(last_epoch_memory)
#
# nets = []
# for m in last_epoch_memory:
#     nets.append({'densities': m['state'], 'lights': m['action']})
# data = {
#     'nets': nets,
#     'rewards sum': reward_sum,
#     'gamma': gamma,
#     'learningEpochs': len(epochs),
#     'learningMethod': 'Monte Carlo',
#     # 'turns':env.turns
# }
#
exportData = ExportData(learningMethod='Monte Carlo TODO', learningEpochs=0, nets=nets, netName='net4',
                        densityName='77')
exportData.saveToJson()

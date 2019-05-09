# 2 odcinki na droge!

import random
import numpy as np
from Env import Env
from env_data import max_time
from services.agentFactory import get_SmartAgents
from services.globals import Globals
from services.jsonSaver import saveToJson


def epoch():
    Globals().time = 0
    env = Env(agents)
    state = env.get_global_action_space()
    memories = []
    for t in range(max_time - 1):
        actions = []
        for agent in agents:
            if not agent.pi is (state[agent.index - 1]):
                agent.pi[state] = random.choice(agent.get_local_action_space())
            else:
                print('powtorka')
            actions.append(agent.pi[state])
        old_state = state
        global_state, local_states, reward = env.step(actions)
    #     state = local_states
    #     memories.append({'state': old_state, 'new_state': state, 'action': actions, 'reward': reward})
    # return memories


def update_returns():
    for i in range(len(agents)):
        agent = agents[i]
        G = 0
        for m in reversed(epoch_memory):
            G = gamma * G + m['reward']
            s = m['state'][i]
            a = m['action'][i]
            if agent.returns is not (s, a):
                agent.returns[(s, a)] = [G]
            else:
                agent.returns[(s, a)].append(G)


def update_pi(is_train):
    for m in epoch_memory:
        s = m['state']
        rand = random.random()
        if (rand < epsilon and is_train):
            pi[s] = random.choice(env.action_space)
        else:
            best_sa_value = -float('inf')
            for action in env.action_space:
                a = hash_(action)
                sa = (s, a)
                sa_value = Q[sa] if Q.has_key(sa) else -float('inf')
                if (sa_value >= best_sa_value):
                    pi[s] = action
                    best_sa_value = sa_value


def count_rewards(epoch_memory):
    rewards_sum = 0
    for m in epoch_memory:
        rewards_sum += m['reward']
    return rewards_sum


agents = get_SmartAgents()
gamma = 1
epsilon = 0.2
# action_space = Env(agents).get_global_action_space()
# state_space = []  # poczotkowo nic [(x, y, z) for x in range(52) for y in range(52) for z in range(52)]
best_score = 0
epochs = range(100)
for e in epochs:
    epoch_memory = epoch()
#     update_returns()
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
# saveToJson('net4', 'den_MC', data)


# def update_Q():
#     for m in epoch_memory:
#         q = np.mean(returns[(m['state'], m['action'])])
#         Q[(m['state'], m['action'])] = q

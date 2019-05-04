# 2 odcinki na droge!

import random
import numpy as np
from Env import Env
from env_data import max_time


def init_Q(state_space, action_space):
    Q = {}
    for s in state_space:
        for a_unhashable in action_space:
            a = hash_(a_unhashable)
            Q[(s, a)] = 0
    return Q


def hash_(action):
    return tuple([tuple(a) for a in action])


def init_returns():
    Returns = {}
    for s in state_space:
        for a_unhashable in action_space:
            a = hash_(a_unhashable)
            Returns[(s, a)] = []
    return Returns


#
# def init_pi():
#     pi = {}
#     for s in state_space:
#         for a_unhashable in action_space:
#             pi[(s)] = a_unhashable
#     return pi


def epoch():
    env = Env()
    state = tuple(env.x[0])
    memories = []
    for t in range(max_time - 1):
        if not pi.has_key(state):
            global_action_space = env.get_global_action_space()
            pi[state] = [random.choice(local_action_space) for local_action_space in global_action_space]
        actions = pi[state]
        old_state = tuple(state)
        global_state, reward = env.step(actions)
        memories.append({'state': old_state, 'new_state': global_state, 'action': hash_(actions), 'reward': reward})
    return memories


def update_returns():
    G = 0
    for m in reversed(memories):
        G = gamma * G + m['reward']
        s = m['state']
        a = m['action']
        if not returns.has_key((s, a)):
            returns[(s, a)] = [G]
        else:
            returns[(s, a)].append(G)


def update_Q():
    for m in memories:
        q = np.mean(returns[(m['state'], m['action'])])
        Q[(m['state'], m['action'])] = q


def update_pi(is_train):
    for m in memories:
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


def count_rewards():
    rewards_sum = 0
    for m in memories:
        rewards_sum += m['reward']
    print(rewards_sum)
    return rewards_sum


gamma = 1
epsilon = 0.2
env = Env()
wins = 0
loses = 0
state_space = []  # poczotkowo nic [(x, y, z) for x in range(52) for y in range(52) for z in range(52)]
action_space = env.get_global_action_space()
Q = {}
returns = {}
# returns = init_returns()
pi = {}
best_score = 0
epochs = range(100)
for e in epochs:
    memories = epoch()
#     update_returns()
#     update_Q()
#     update_pi(True)
#     count_rewards()
# update_pi(False)
# memories = epoch()  # last epoch
# reward_sum = count_rewards()


# print(reward_sum)
# print(memories)
# nets = []
# for m in memories:
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
# saveToJson('net3', 'den1', data)

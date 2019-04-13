import matplotlib.pyplot as plt
import gym
import random
import numpy as np
from env import Env
from jsonSaver import saveToJson


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


def init_pi():
    pi = {}
    for s in state_space:
        for a_unhashable in action_space:
            pi[(s)] = a_unhashable
    return pi


def epoch():
    env = Env(10)
    state = tuple(env.x[0])
    memories = []
    for t in range(T):
        action = pi[state]
        old_state = tuple(state)
        state, reward = env.step(action)
        state = tuple(state)
        memories.append({'state': old_state, 'new_state': state, 'action': hash_(action), 'reward': reward})
    return memories


def update_returns():
    G = 0
    for m in reversed(memories):
        G = gamma * G + m['reward']
        s = m['state']
        a = m['action']
        returns[(m['state'], m['action'])].append(G)


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
    return rewards_sum
    # print(rewards_sum)


gamma = 1
epsilon = 0.1
env = Env(10)
wins = 0
loses = 0
state_space = [(x, y, z) for x in range(52) for y in range(52) for z in range(52)]
action_space = env.action_space
Q = init_Q(state_space, action_space)
returns = init_returns()
pi = init_pi()
T = 10
best_score = 0
epochs = range(20)
for e in epochs:
    memories = epoch()
    update_returns()
    update_Q()
    update_pi(True)
    # count_rewards()
update_pi(False)
memories = epoch()  # last epoch
reward_sum = count_rewards()
print(reward_sum)
print(memories)
lines = []
for m in memories:
    lines.append({'densities': m['state'], 'lights': m['action']})
data = {
    'lines': lines,
    'rewards sum': reward_sum,
    'gamma': gamma,
    'learningEpochs': len(epochs),
    'learningMethod': 'Monte Carlo',
}

saveToJson('net1', 'den1', data)

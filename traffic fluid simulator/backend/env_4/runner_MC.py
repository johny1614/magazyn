# 2 odcinki na droge!

import random
import numpy as np
from Env import Env
from env_data import max_time
from services.agentFactory import get_SmartAgents


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
    env = Env(agents)
    state = tuple([agent.local_state for agent in agents])
    memories = []
    for t in range(max_time - 1):
        actions=[]
        for agent in agents:
            if not agent.pi.has_key(state[agent.index-1]):
                print(agent.getLocalActionSpace())
                agent.pi[state]=random.choice(agent.getLocalActionSpace())
            else:
                print('powtorka')
            actions.append(agent.pi[state])
        old_state = tuple(state)
        global_state, local_states, reward = env.step(actions)
        state = tuple(local_states)
        memories.append({'state': old_state, 'new_state': state, 'action': actions, 'reward': reward})
    return memories


def update_returns():
    for i in range(len(agents)):
        agent=agents[i]
        G = 0
        for m in reversed(memories):
            G = gamma * G + m['reward']
            s = m['state'][i]
            a = m['action'][i]
            print(a)
            if not returns.has_key((s, a)):
                agent.returns[(s, a)] = [G]
            else:
                print('yes')
                agent.returns[(s, a)].append(G)


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


agents = get_SmartAgents()
gamma = 1
epsilon = 0.2
wins = 0
loses = 0
action_space = Env(agents).get_global_action_space()
state_space = []  # poczotkowo nic [(x, y, z) for x in range(52) for y in range(52) for z in range(52)]
Q = {}
returns = {}
# returns = init_returns()
pi = {}
best_score = 0
epochs = range(100)
for e in epochs:
    memories = epoch()
    update_returns()
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

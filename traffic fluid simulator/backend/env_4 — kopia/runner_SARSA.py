# 2 odcinki na droge!

import random
from Env import Env


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
    env = Env(state_arr_size, max_time)
    state = tuple(env.x[0])
    memories = []
    for t in range(max_time - 1):
        if not pi.has_key(state):
            pi[state]=random.choice(env.action_space)
        action=pi[state]
        old_state = tuple(state)
        # print('action',action)
        # print('hash',hash_(action))
        state,reward = env.step(hash_(action))
        state = tuple(state)
        # print('state',state)
        memories.append({'state': old_state, 'new_state': state, 'action': hash_(action), 'reward': reward})
    return memories


def update_returns():
    G = 0
    for m in reversed(memories):
        G = gamma * G + m['reward']
        s = m['state']
        a = m['action']
        if not returns.has_key((s,a)):
            returns[(s, a)]=[G]
        else:
            returns[(s, a)].append(G)


def update_Q(s,a,r,s_prim,a_prim):
    if not Q.has_key(tuple([a, s])):
        Q[s, a] = r
    else:
        if not Q.has_key(tuple([a_prim, s_prim])):
            Q[a_prim, s_prim]=0
        Q[s, a] = Q[s, a] + alfa*(r+gamma*Q[s_prim, a_prim])
        # pi[state] = random.choice(env.action_space)
    # action = pi[state]

    # print('a')
    # for m in memories:
    #     q = np.mean(returns[(m['state'], m['action'])])
    #     Q[(m['state'], m['action'])] = q



# def update_pi(is_train):
#     for m in memories:
#         s = m['state']
#         rand = random.random()
#         if (rand < epsilon and is_train):
#             pi[s] = random.choice(env.action_space)
#         else:
#             best_sa_value = -float('inf')
#             for action in env.action_space:
#                 a = hash_(action)
#                 sa = (s, a)
#                 sa_value = Q[sa] if Q.has_key(sa) else -float('inf')
#                 if (sa_value >= best_sa_value):
#                     pi[s] = action
#                     best_sa_value = sa_value
def count_rewards():
    rewards_sum = 0
    for m in memories:
        rewards_sum += m['reward']
    return rewards_sum
def get_action(state,is_train=True):
    rand=random.random()
    if (rand < epsilon and is_train):
        action= random.choice(env.action_space)
    else:
        action= greedy_action(state)
    return hash_(action)
def greedy_action(state):
    keys_of_state=[qkey for qkey in Q.keys() if qkey[0]==state]
    if(len(keys_of_state)==0):
        return random.choice(env.action_space)
    best_q_value=-9999
    best_action_key=None
    for key in keys_of_state:
        actionValue=Q[key]
        if(actionValue>=best_q_value):
            best_q_value=actionValue
            best_action_key=key[1]
    return best_action_key
alfa=0.4
max_time = 30
timeSpace = range(max_time)
gamma = 1
epsilon = 0.1
env = Env( max_time)
Q = {}
pi = {}
best_score = 0
epochs = range(20000)
for e in epochs:
    env = Env(max_time+1)
    s = tuple(env.x[0])
    a = get_action(s)
    sumRewards=0
    for t in timeSpace:
        s_prim,r=env.step(a)
        sumRewards+=r
        s_prim=tuple(s_prim)
        a_prim = get_action(s_prim)
        update_Q(s,a,r,s_prim,a_prim)
        s=s_prim
        a=a_prim
    # print('rewards',sumRewards)

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
# saveToJson('net3', 'den_SARSA', data)

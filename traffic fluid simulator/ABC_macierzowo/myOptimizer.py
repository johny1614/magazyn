import matplotlib.pyplot as plt
import gym
import random
import numpy as np
from env import Env
def init_Q(state_space,action_space):
    Q={}
    for s in state_space:
        for a_unhashable in action_space:
            a=hash_(a_unhashable)
            Q[(s,a)] = 0
    return Q
def hash_(action):
    return tuple([tuple(a) for a in action])
def init_returns():
    Returns={}
    for s in state_space:
        for a_unhashable in action_space:
            a=hash_(a_unhashable)
            Returns[(s,a)] = []
    return Returns
def init_pi():
    pi = {}
    for s in state_space:
        for a_unhashable in action_space:
            pi[(s)] = a_unhashable
    return pi
def epoch():
    env = Env(10)
    state=tuple(env.x[0])
    memories=[]
    for t in range(T):
        action=pi[state]
        old_state=tuple(state)
        state,reward = env.step(action)
        state=tuple(state)
        memories.append({'state':old_state,'new_state':state,'action':hash_(action),'reward':reward})
    return memories
def update_returns():
    G=0
    for m in reversed(memories):
        G=gamma*G+m['reward']
        s = m['state']
        a = m['action']
        returns[(m['state'],m['action'])].append(G)
def update_Q():
    for m in memories:
        q=np.mean(returns[(m['state'],m['action'])])
        Q[(m['state'],m['action'])]=q
def update_pi():
    for m in memories:
        s=m['state']
        rand=random.random()
        if(rand<epsilon):
            pi[s]=random.choice(env.action_space)
        else:
            best_sa_value=-float('inf')
            for action in env.action_space:
                a=hash_(action)
                sa=(s,a)
                sa_value=Q[sa] if Q.has_key(sa) else -float('inf')
                if(sa_value>=best_sa_value):
                    pi[s]=action
                    best_sa_value=sa_value
def count_rewards():
    rewards_sum=0
    for m in memories:
        rewards_sum+=m['reward']
    print(rewards_sum)
gamma=1
epsilon=0.1
env=Env(10)
wins=0
loses=0
state_space=[ (x,y,z) for x in range(52) for y in range(52) for z in range(52)]
action_space=env.action_space
Q=init_Q(state_space,action_space)
returns=init_returns()
pi=init_pi()
T=10
best_score=0
epochs=range(100)
for e in epochs:
    memories=epoch()
    update_returns()
    update_Q()
    update_pi()
    count_rewards()

# def init_pi():
#     pi={}
#     actionSpace = [0, 1]  # stick or hit
#     agentSumSpace = [i for i in range(4, 32)]
#     dealerShowCardSpace = [i + 1 for i in range(10)]
#     agentAceSpace = [False, True]
#     for points in agentSumSpace:
#         for dealerCard in dealerShowCardSpace:
#             for ace in agentAceSpace:
#                 action=random.choice(actionSpace)
#                 pi[((points, dealerCard, ace))] = action
#     return pi # stanow jest 18*10*2=360
# def epoch():
#     global wins
#     global loses
#     state =env.reset()
#     memory=[]
#     for t in range(100):
#         old_state=state
#         action=pi[old_state]
#         state, reward, done, info = env.step(action)
#         sa=(state,pi[old_state])
#         memory.append({'state':old_state,'new_state':state,'action':action,'t':t,'reward':reward})
#         if(done):
#             if(reward==1):
#                 wins=wins+1
#             if(reward==-1):
#                 loses=loses+1
#             return memory
# def update_Q():
#     G=0
#     for memory in reversed(memory_rewards):
#         G=gamma*G+memory['reward']
#         sa=(memory['state'],memory['action'])
#         returns[sa]=[G] if not returns.has_key(sa) else returns[sa] + [G]
#         q[sa]=np.mean(returns[sa])
# def update_pi():
#     for state in pi:
#         if(random.random()<epsilon):
#             pi[state]=random.choice(actionSpace)
#         else:
#             best_sa_value=-float('inf')
#             for action in actionSpace:
#                 sa=(state,action)
#                 sa_value=q[sa] if q.has_key(sa) else -float('inf')
#                 if(sa_value>=best_sa_value):
#                     pi[state]=action
#                     best_sa_value=sa_value
# win_rates=[]
# max_T=3000
# epochs=range(max_T)
# actionSpace = [0, 1]  # stick or hit
# q = init_Q()
# returns = init_returns()
# pi = init_pi()
# epsilon=0.1
# gamma=1
# env = gym.make('Blackjack-v0')
# for epoch_number in range(max_T):
#     memory_rewards=epoch()
#     update_Q()
#     update_pi()
#     win_rates.append(float(wins)/(loses+wins))
# print('win rate',float(wins)/(loses+wins)) # with eps=0.1 we have 3000 epochs = 0.38, 10 000 - 0.4, 100 000 - 0.443
# # plt.plot(epochs, win_rates)
# # plt.show()
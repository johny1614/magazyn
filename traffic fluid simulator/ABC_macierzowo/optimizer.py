import numpy as np
from env import Env
from matrix import A_a_green,A_b_green
def find_best_action(actions):

def predict():
    delta=0
    for state in V:
        action=policy[state]
        future_state,reward=env.dry_step(action)
        future_state_V=V.get(tuple(future_state),0)
        V[state]=future_state_V+gamma*reward
def control():
    V_pi=V
    new_V = {key: 0 for key in V}
    policy_stable = 0
    for state in new_V:
        old_action=policy[state]
        find_best_action([A_a_green,A_b_green])
gamma=1
n=10
teta=0.8
env=Env(n)

# rewardSum=0
policy={tuple(env.x[0]):A_a_green}
V={tuple(env.x[0]):0}
# print(V)
# for t in range(1,n):
    # for state in V:
predict()
control()
    # for
    # A=A_a_green if t%2==0 else A_b_green
    # reward,state = env.step(A)
    # V{state}=
    # rewardSum += reward
# print(rewardSum)
# print(policy)

# only A_a_green - 43
# only A_b_green - 36
# na zmiane - 73
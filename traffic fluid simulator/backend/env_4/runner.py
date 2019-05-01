from env import Env
import random
def hash_(action):
    return tuple([tuple(a) for a in action])

max_time=30
env = Env(max_time)
for time in range(max_time-1):
    env.get_global_action_space()
    # a = random.choice(env.getActionSpace())
    # state,r,action = env.step(a)
    # print('a',action)
    # print('s',state)

from env import Env
import random
def hash_(action):
    return tuple([tuple(a) for a in action])

max_time=15
env = Env(max_time)
for time in range(max_time-1):
    action = hash_(random.choice(env.action_space))
    state,reward = env.step(action)


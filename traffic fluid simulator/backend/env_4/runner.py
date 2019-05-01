from env import Env
import random
def hash_(action):
    return tuple([tuple(a) for a in action])

max_time=30
env = Env(max_time)
for time in range(max_time-1):
    global_action_space=env.get_global_action_space()
    actions=[random.choice(local_action_space) for local_action_space in global_action_space]
    global_state,r= env.step(actions)
    print(global_state.x)

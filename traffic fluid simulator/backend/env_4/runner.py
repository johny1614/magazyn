from SaveData import SaveData
from env import Env
import random

from jsonSaver import saveToJson


def hash_(action):
    return tuple([tuple(a) for a in action])


save_data = SaveData(learningEpochs=0, learningMethod='Random')
max_time = 30
env = Env(max_time)
for time in range(max_time - 1):
    global_action_space = env.get_global_action_space()
    actions = [random.choice(local_action_space) for local_action_space in global_action_space]
    global_state, r = env.step(actions)
    save_data.add_net(global_state)
saveToJson('net4','den1',save_data)
env.pretty_print()
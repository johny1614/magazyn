from model.SaveData import SaveData
from Env import Env
import random

from env_data import max_time
from services.jsonSaver import saveToJson


def hash_(action):
    return tuple([tuple(a) for a in action])


save_data = SaveData(learningEpochs=0, learningMethod='Random')
env = Env()
save_data.nets.append({'densities': tuple(env.x[0])})
for time in range(max_time - 1):
    global_action_space = env.get_global_action_space()
    actions = [random.choice(local_action_space) for local_action_space in global_action_space]
    if actions[0] == 'wait':
        actions = ['wait'] * 3
    elif time < 14:
        actions = [1, 1, 1]
    elif time >= 20 and actions[0] != 'wait':
        actions = [3, 3, 3]
    elif time >= 14 and actions[0] != 'wait':
        actions = [2, 2, 2]
    global_state, r = env.step(actions)
    save_data.add_net(global_state)
save_data.attach_lights(env.A_storage)
saveToJson('net4', 'den1', save_data)
print(env.x[0])
# env.pretty_print()
# env.pretty_print_4()

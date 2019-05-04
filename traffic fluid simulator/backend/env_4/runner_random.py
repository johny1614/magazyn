from model.SaveData import SaveData
from Env import Env
import random

from env_data import max_time


def hash_(action):
    return tuple([tuple(a) for a in action])


def random_epoch():
    env = Env()
    save_data.nets.append({'densities': tuple(env.x[0])})
    for time in range(max_time - 1):
        global_action_space = env.get_global_action_space()
        actions = [random.choice(local_action_space) for local_action_space in global_action_space]
        global_state, r = env.step(actions)
        save_data.add_net(global_state)
    save_data.attach_lights(env.A_storage)
    cars_out = sum(env.y)
    return cars_out

best_cars_out = 0
learningEpochs = 10000
# for i in
save_data = SaveData(learningEpochs=0, learningMethod='Random')
env = Env()
save_data.nets.append({'densities': tuple(env.x[0])})
for epoch_no in range(learningEpochs):
    cars_out=random_epoch()
    best_cars_out=cars_out if cars_out>best_cars_out else best_cars_out
print(best_cars_out)

# best score: 2832

# saveToJson('net4','den1',save_data)
# print(env.x[0])
# env.pretty_print()
# env.pretty_print_4()

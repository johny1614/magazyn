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
    if(actions[0]=='wait'):
        actions=['wait']*3
    elif(time<14):
        actions=[1,1,1]
    elif(time>=14 and actions[0]!='wait'):
        actions=[2,2,2]
    global_state, r = env.step(actions)
    save_data.add_net(global_state)
saveToJson('net4','den1',save_data)
# env.pretty_print()
env.pretty_print_4()
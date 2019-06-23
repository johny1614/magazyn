import os

import numpy as np

import env_settings

os.environ["PATH"] += os.pathsep + 'C:/Graphviz/bin'
from typing import List
from Env import Env
from env_settings import max_time
from model.SmartAgent import SmartAgent
from services.agentFactory import get_SmartAgents
from services.globals import Globals

ActionInt = int

def epoch():
    Globals().time = 0
    env = Env(agents)
    env.u = env_settings.u_all_2
    # env.u = env_settings.u_v1
    for t in range(max_time):
        actions: List[ActionInt] = [agent.get_action(agent.local_state) for agent in agents]
        env.step(actions)
    Globals().epochs_done += 1
    return env


agents: List[SmartAgent] = get_SmartAgents()
epochs = range(1400)
for e in epochs:
    Globals().epsilon = 1
    env: Env = epoch()
    for agent in env.agents:
        agent.reshape_rewards()
    print(e)

for i in range(len(agents)):
    print(i)
    filename='static_files/x_batch_agent_'+str(i)+'.txt'
    x_batch, y_batch = agent.full_batch()
    np.savetxt(filename,x_batch,delimiter=',')
    filename='static_files/y_batch_agent_'+str(i)+'.txt'
    np.savetxt(filename,y_batch,delimiter=',')


# env.update_global_memory_rewards()
# x_batch, y_batch = agents[0].full_batch()
# np.savetxt('static_files/x_batch_agent_0.txt',Globals().x_batch,delimiter=',')
# np.savetxt('static_files/y_batch_agent_0.txt',Globals().y_batch,delimiter=',')

import random
from typing import List
import matplotlib.pyplot as plt
import numpy as np
import env_settings
from Env import Env
from model.Action import yellow, ActionInt
from model.ExportData import ExportData
from model.SmartAgent import SmartAgent
from services.agentFactory import get_SmartAgents, get_LearnSmartAgents
from services.globals import Globals


def epoch(agents, time, u=None):
    if u is None:
        u = Globals().get_u(time)
    Globals().time = 0
    env = Env(agents)
    env.u = u
    for t in range(time):
        actions: List[ActionInt] = [agent.get_action(agent.local_state) for agent in agents]
        if actions[0] != yellow:
            Globals().actions_memory[int(actions[0])] += 1
        env.step(actions)
    Globals().epochs_learn_done += 1
    return env


def my_epoch(agents, time, u=None):
    if u is None:
        u = Globals().get_u(time)
    Globals().time = 0
    env = Env(agents)
    env.u = u
    random_number = random.random()
    for t in range(time):
        if t == 20 or t == 22 or t == 23 or t == 24:
            # print('rn', random_number)
            actions = [0, 0, 0]
            if random_number > 0.5:
                actions = [0, 0, 0]
        else:
            actions = [2, 0, 0]
            # print('stan',env.global_state[0].to_learn_array(agents[0]))
        env.step(actions)
    Globals().epochs_learn_done += 1
    return env


def save_batches(agents, actual_number=''):
    for i in range(len(agents)):
        filename = 'static_files/x_batch_agent_' + str(i) + '_' + str(actual_number) + '.txt'
        x_batch, y_batch = agents[i].full_batch_no_yellow()
        np.savetxt(filename, x_batch, delimiter=',')
        filename = 'static_files/y_batch_agent_' + str(i) + '_' + str(actual_number) + '.txt'
        np.savetxt(filename, y_batch, delimiter=',')


def generate_random_epochs(learntAgents=False, save_front_json=False, epochs=range(1)):
    reshaping = True
    cars_outs = []
    rewards = []
    rewards_mean = []
    if learntAgents:
        agents: List[SmartAgent] = get_LearnSmartAgents()
    else:
        agents: List[SmartAgent] = get_SmartAgents()
    for agent in agents:
        agent.memories = []
    for e in epochs:
        Globals().epsilon = 1
        env: Env = epoch(agents, u=Globals().get_u(Globals().vp.max_time_learn), time=Globals().vp.max_time_learn)
        for agent in env.agents:
            agent.reshape_rewards()
        if save_front_json:
            exportData = ExportData(learningMethod='DQN', learningEpochs=0, nets=env.global_memories,
                                    netName='politechnika',
                                    densityName='random_now' + str(Globals().greedy_run_no))
            exportData.saveToJson()
        env.remember_memory()
    save_batches(agents)
    return agents


if __name__ == "__main__":
    generate_random_epochs(save_front_json=False)

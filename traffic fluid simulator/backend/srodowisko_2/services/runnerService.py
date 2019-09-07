import random
from typing import List
from Env import Env
from env_settings import max_time
from model.Action import ActionInt
from model.ExportData import ExportData
from model.SmartAgent import SmartAgent
from services.agentFactory import get_SmartAgents, get_LearnSmartAgents
from services.globals import Globals
import numpy as np


def epoch_greedy(env) -> Env:
    Globals().time = 0
    for t in range(max_time):
        actions: List[ActionInt] = [agent.get_action(state=agent.local_state,greedy=True) for agent in env.agents]
        env.step(actions)
    return env


def run_learnt_greedy(saveJson=True):
    model_file_names = ['static_files/model-agent0.h5']
    agents = get_LearnSmartAgents(model_file_names)
    env = Env(agents)
    epoch_greedy(env)
    rewards_sum, rewards_mean = count_rewards(env)
    cars_out = env.cars_out
    if saveJson:
        exportData = ExportData(learningMethod='DQN', learningEpochs=0, nets=env.global_memories,
                                netName='env2',
                                densityName='learnt_' + str(Globals().greedy_run_no))
        exportData.saveToJson()
    Globals().greedy_run_no += 1
    print(
        f'gready run {Globals().greedy_run_no} - rewards_mean:{round(rewards_mean, 2)} rewards_sum:{round(rewards_sum,0)} cars_out:{round(cars_out, 0)} układ opuściło procentowo pojazdów:{cars_out / sum(sum(Globals().u))}')
    return rewards_mean, rewards_sum, cars_out

def epoch(agents, u=Globals().u):
    Globals().time = 0
    env = Env(agents)
    env.u = u
    for t in range(max_time):
        actions: List[ActionInt] = [agent.get_action(agent.local_state) for agent in agents]
        env.step(actions)
    Globals().epochs_done += 1
    return env

def count_rewards(env):
    memsum = 0
    i = 0
    for agent in env.agents:
        for mem in agent.memories:
            i += 1
            memsum += mem.reward
    return memsum, memsum / i


def save_batches(agents):
    for i in range(len(agents)):
        filename = 'static_files/x_batch_agent_' + str(i) + '.txt'
        x_batch, y_batch = agents[i].full_batch_no_yellow(only_learn_usable=True)
        np.savetxt(filename, x_batch, delimiter=',')
        filename = 'static_files/y_batch_agent_' + str(i) + '.txt'
        np.savetxt(filename, y_batch, delimiter=',')


def generate_random_epochs(learntAgents=False, save_front_json=False, epochs=range(1), plotting=False, u=Globals().u,
                           clear_memory=True):
    reshaping = True
    cars_outs = []
    rewards = []
    rewards_mean = []
    if learntAgents:
        agents: List[SmartAgent] = get_LearnSmartAgents()
    else:
        agents: List[SmartAgent] = get_SmartAgents()
    if clear_memory:
        for agent in agents:
            agent.memories = []
    for e in epochs:
        Globals().epsilon = 1
        env: Env = epoch(agents, u=u)
        if reshaping:
            for agent in env.agents:
                agent.reshape_rewards()
        if save_front_json:
            exportData = ExportData(learningMethod='DQN', learningEpochs=0, nets=env.global_memories,
                                    netName='net14',
                                    densityName='random_updated' + str(e))
            exportData.saveToJson()
        env.remember_memory()
        if save_front_json:
            exportData = ExportData(learningMethod='DQN', learningEpochs=0, nets=env.global_memories,
                                    netName='net14',
                                    densityName='random_' + str(e))

            exportData.saveToJson()
        if plotting:
            cars_outs.append(env.cars_out)
            rewards.append(env.count_summed_rewards()[0])
            rewards_mean.append(env.count_summed_rewards()[1])
        Globals().actual_epoch_index += 1
    save_batches(agents)
    return agents

import numpy as np
from typing import List
from Env import Env
from Utils import count_rewards
from model import SmartAgent
from model.Action import yellow, ActionInt
from model.ExportData import ExportData
from services.agentFactory import get_LearnSmartAgents, get_SmartAgents
from services.globals import Globals


def epoch_greedy(env) -> Env:
    Globals().time = 0
    actions_count_0 = [0, 0, 0, 0, 0]
    actions_count_1 = [0, 0, 0, 0, 0]
    actions_count_2 = [0, 0, 0, 0, 0]
    actions_count_3 = [0, 0, 0, 0, 0]
    for t in range(Globals().vp.max_time_greedy):
        actions: List[ActionInt] = [agent.get_action(state=agent.local_state, greedy=True) for agent in env.agents]
        env.step(actions)
        if actions[0] != yellow:
            actions_count_0[int(actions[0])] += 1
        else:
            actions_count_0[-1] += 1
        if actions[1] != yellow:
            actions_count_1[int(actions[1])] += 1
        else:
            actions_count_1[-1] += 1
        if actions[2] != yellow:
            actions_count_2[int(actions[2])] += 1
        else:
            actions_count_2[-1] += 1
        if actions[3] != yellow:
            actions_count_3[int(actions[3])] += 1
        else:
            actions_count_3[-1] += 1
    return env.u
    print('akcje podjete', [actions_count_0, actions_count_1, actions_count_2, actions_count_3])


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


def save_batches(agents, actual_number=''):
    for i in range(len(agents)):
        filename = 'static_files/x_batch_agent_' + str(i) + '_' + str(actual_number) + '.txt'
        x_batch, y_batch = agents[i].full_batch_no_yellow()
        np.savetxt(filename, x_batch, delimiter=',')
        filename = 'static_files/y_batch_agent_' + str(i) + '_' + str(actual_number) + '.txt'
        np.savetxt(filename, y_batch, delimiter=',')


def generate_random_epochs(learntAgents=False, save_front_json=False, epochs=range(1)):
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
                                    netName='env4',
                                    densityName='random_now' + str(Globals().greedy_run_no))
            exportData.saveToJson()
        env.remember_memory()
    save_batches(agents)
    return agents


def run_learnt_greedy(saveJson=True):
    Globals().cars_out_memory = []
    model_file_names = ['static_files/model-agent0.h5', 'static_files/model-agent1.h5', 'static_files/model-agent2.h5',
                        'static_files/model-agent3.h5']
    agents = get_LearnSmartAgents(model_file_names)
    env = Env(agents)
    u = epoch_greedy(env)
    rewards_sum, rewards_mean = count_rewards(env)
    cars_out = env.cars_out
    if saveJson:
        exportData = ExportData(learningMethod='DQN', learningEpochs=0, nets=env.global_memories,
                                netName='env4',
                                densityName='learnt_' + str(Globals().greedy_run_no))
        exportData.saveToJson()
    maximum_possible_cars_out = Globals().u_value * Globals().vp.max_time_greedy * 8
    print(
        f'gready run {Globals().greedy_run_no} - rewards_mean:{round(rewards_mean, 2)} rewar'
        f'ds_sum:{round(rewards_sum, 0)}. Do układu wjechało {round(sum(sum(u)), 0)} pojazdów.'
        f' Wyjechało {round(cars_out, 0)}. Układ opuściło pr'
        f'ocentowo pojazdów:{round(100 * cars_out / maximum_possible_cars_out, 2)}')
    Globals().greedy_run_no += 1
    return rewards_mean, rewards_sum, cars_out, agents, sum(sum(u))

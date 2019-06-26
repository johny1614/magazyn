import os

import numpy as np
import matplotlib.pyplot as plt

import env_settings
from model.ExportData import ExportData

os.environ["PATH"] += os.pathsep + 'C:/Graphviz/bin'
from typing import List
from Env import Env
from env_settings import max_time
from model.SmartAgent import SmartAgent
from services.agentFactory import get_SmartAgents, get_LearnSmartAgents
from services.globals import Globals

ActionInt = int


def epoch(agents, u=env_settings.u_all_2):
    Globals().time = 0
    env = Env(agents)
    env.u = u
    for t in range(max_time):
        actions: List[ActionInt] = [agent.get_action(agent.local_state) for agent in agents]
        env.step(actions)
    Globals().epochs_done += 1
    return env


def generate_random_epochs(learntAgents=False, save_front_json=False, epochs=range(200), plotting=False):
    # learntAgents = True
    # save_json = True
    # plotting=True
    cars_outs = []
    rewards = []
    rewards_mean = []

    if learntAgents:
        agents: List[SmartAgent] = get_LearnSmartAgents()
    else:
        agents: List[SmartAgent] = get_SmartAgents()
    for e in epochs:
        Globals().epsilon = 1
        env: Env = epoch(agents, u=env_settings.u_all_4)
        for agent in env.agents:
            agent.reshape_rewards()
        env.update_memory_rewards()
        env.remember_memory()
        if save_front_json:
            exportData = ExportData(learningMethod='DQN', learningEpochs=0, nets=env.global_memories,
                                    netName='net4',
                                    densityName='random_' + str(e))
            exportData.saveToJson()
        x_batch, y_batch = agents[0].memory_to_minibatch_with_oranges()
        if plotting:
            cars_outs.append(env.cars_out)
            print('rew',env.count_summed_rewards()[0])
            print('cars_out',env.cars_out)
            rewards.append(env.count_summed_rewards()[0])
            rewards_mean.append(env.count_summed_rewards()[1])

    for i in range(len(agents)):
        # print('i',i)
        filename = 'static_files/x_batch_agent_' + str(i) + '.txt'
        x_batch, y_batch = agents[i].full_batch()
        np.savetxt(filename, x_batch, delimiter=',')
        filename = 'static_files/y_batch_agent_' + str(i) + '.txt'
        np.savetxt(filename, y_batch, delimiter=',')
    if plotting:
        plt.plot(cars_outs)
        plt.title('Ilość pojazdów opuszczających układ - losowe akcje')
        plt.savefig('img_cars_out_random.png')
        plt.close()
        plt.plot(rewards_mean)
        plt.title('Średnia nagroda za akcję - losowe akcje')
        plt.savefig('img_rewards_mean_random.png')
        plt.close()
        plt.plot(rewards)
        plt.title('Suma nagród - losowe akcje')
        plt.savefig('img_rewards_random.png')
        plt.close()

        # filename = 'static_files/y_batch_agent_batch_time' + str(i) + '.txt'
        # np.savetxt(filename, (x_batch, y_batch), delimiter=',')
    # full_batch=agents[0].full_batch()
    # orange_batch = agents[0].memory_to_minibatch_with_oranges()
    # a = 2
    # env.update_global_memory_rewards()
    # x_batch, y_batch = agents[0].full_batch()
    # np.savetxt('static_files/x_batch_agent_0.txt',Globals().x_batch,delimiter=',')
    # np.savetxt('static_files/y_batch_agent_0.txt',Globals().y_batch,delimiter=',')


if __name__ == "__main__":
    generate_random_epochs()

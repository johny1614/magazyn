from typing import List
import matplotlib.pyplot as plt
import numpy as np
import env_settings
from Env import Env
from model.ExportData import ExportData
from model.SmartAgent import SmartAgent
from services.agentFactory import get_SmartAgents, get_LearnSmartAgents
from services.globals import Globals

ActionInt = int


def epoch(agents, time, u=None):
    if u is None:
        u = Globals().get_u(time)
    Globals().time = 0
    env = Env(agents)
    env.u = u
    for t in range(time):
        actions: List[ActionInt] = [agent.get_action(agent.local_state) for agent in agents]
        env.step(actions)
    Globals().epochs_done += 1
    return env


def save_batches(agents):
    for i in range(len(agents)):
        filename = 'static_files/x_batch_agent_' + str(i) + '.txt'
        x_batch, y_batch = agents[i].full_batch_no_orange(only_learn_usable=True)
        np.savetxt(filename, x_batch, delimiter=',')
        filename = 'static_files/y_batch_agent_' + str(i) + '.txt'
        np.savetxt(filename, y_batch, delimiter=',')


def generate_random_epochs(learntAgents=False, save_front_json=False, epochs=range(1), plotting=False, reshaping=False,
                           actions=None, clear_memory=True):
    # save_front_json = True
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
    # print(agents[0].orange_phase_duration)
    for e in epochs:
        Globals().epsilon = 1
        env: Env = epoch(agents, u=Globals().get_u(Globals().vp().max_time_learn), time=Globals().vp().max_time_learn)
        if reshaping:
            for agent in env.agents:
                agent.reshape_rewards()
        action_0_rewards = [net.rewards[0] for net in env.global_memories if net.actions == [0]]
        action_1_rewards = [net.rewards[0] for net in env.global_memories if net.actions == [1]]
        # print('mean 0', np.mean(action_0_rewards))
        # print('mean 1', np.mean(action_1_rewards))
        # if np.mean(action_0_rewards) > np.mean(action_1_rewards):
        #     print('kupa')
        # else:
        #     print('ok')
        # if save_front_json and e == 1:
        #     exportData = ExportData(learningMethod='DQN', learningEpochs=0, nets=env.global_memories,
        #                             netName='net16',
        #                             densityName='random_updated' + str(e))
        #     exportData.saveToJson()
        if save_front_json:
            exportData = ExportData(learningMethod='DQN', learningEpochs=0, nets=env.global_memories,
                                    netName='net16',
                                    densityName='random_now' + str(e))

            exportData.saveToJson()
            print('doneeeeeee',e)
        env.remember_memory()
        if plotting:
            cars_outs.append(env.cars_out)
            rewards.append(env.count_summed_rewards()[0])
            rewards_mean.append(env.count_summed_rewards()[1])
        Globals().actual_epoch_index += 1

        # action_0_rewards = [net.rewards[0] for net in env.global_memories if net.actions == [0]]
        # action_1_rewards = [net.rewards[0] for net in env.global_memories if net.actions == [1]]
        # print('mean 0', np.mean(action_0_rewards))
        # print('mean 1', np.mean(action_1_rewards))
        # if np.mean(action_0_rewards)>np.mean(action_1_rewards):
        #     print('kupa')
        # else:
        #     print('ok')
        # print('cars_out random', env.cars_out)
        # for agent in agents:
        #     highest_x=max([max(mem.state.to_learn_array(agent)[0]) for mem in agent.memories])
        #     print('highest_x',highest_x)
    save_batches(agents)
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
    # if any(x for x in [mem.reward for mem in agents[0].memories] if x > 10.1):
    #     print("weeeeeeeeeeee")
    return agents


if __name__ == "__main__":
    # while True:
    generate_random_epochs(save_front_json=True)
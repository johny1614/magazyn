from typing import List
import matplotlib.pyplot as plt
import numpy as np
import env_settings
from Env import Env
from env_settings import max_time
from model.ExportData import ExportData
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
        # print(f't:{t} a: {actions}')
        env.step(actions)
    Globals().epochs_done += 1
    return env


def do_epoch(agents):
    # save_front_json=True
    cars_outs = []
    rewards = []
    rewards_mean = []
    env: Env = epoch(agents, u=env_settings.u)
    for agent in env.agents:
        agent.reshape_rewards()
    env.update_memory_rewards()
    env.remember_memory()
    exportData = ExportData(learningMethod='Monte Carlo On-Policy', learningEpochs=0, nets=env.global_memories,
                            netName='net11',
                            densityName='MC_' + str(Globals().run_no))
    exportData.saveToJson()
    Globals().run_no+=1
    return env
    #     if plotting:
    #         cars_outs.append(env.cars_out)
    #         print('rew', env.count_summed_rewards()[0])
    #         print('cars_out', env.cars_out)
    #         rewards.append(env.count_summed_rewards()[0])
    #         rewards_mean.append(env.count_summed_rewards()[1])
    #
    # for i in range(len(agents)):
    #     filename = 'static_files/x_batch_agent_' + str(i) + '.txt'
    #     x_batch, y_batch = agents[i].last_epoch_batch()
    #     np.savetxt(filename, x_batch, delimiter=',')
    #     filename = 'static_files/y_batch_agent_' + str(i) + '.txt'
    #     np.savetxt(filename, y_batch, delimiter=',')
    # if plotting:
    #     plt.plot(cars_outs)
    #     plt.title('Ilość pojazdów opuszczających układ - losowe akcje')
    #     plt.savefig('img_cars_out_random.png')
    #     plt.close()
    #     plt.plot(rewards_mean)
    #     plt.title('Średnia nagroda za akcję - losowe akcje')
    #     plt.savefig('img_rewards_mean_random.png')
    #     plt.close()
    #     plt.plot(rewards)
    #     plt.title('Suma nagród - losowe akcje')
    #     plt.savefig('img_rewards_random.png')
    #     plt.close()


if __name__ == "__main__":
    generate_random_epochs()

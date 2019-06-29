from Env import Env
from model.ExportData import ExportData
from runner import epoch_greedy
from services.agentFactory import get_LearnSmartAgents
import numpy as np

from services.globals import Globals


def count_rewards(env):
    memsum = 0
    i = 0
    for agent in env.agents:
        for mem in agent.memories:
            i += 1
            memsum += mem.reward
    return memsum, memsum / i


def run_learnt_greedy(saveJson=False):
    model_file_names = ['static_files/model-agent0.h5', 'static_files/model-agent1.h5', 'static_files/model-agent2.h5']
    agents = get_LearnSmartAgents(model_file_names)
    env = Env(agents)
    epoch_greedy(env)
    env.update_memory_rewards()
    rewards_sum, rewards_mean = count_rewards(env)
    cars_out = env.cars_out
    if saveJson:
        exportData = ExportData(learningMethod='DQN', learningEpochs=0, nets=env.global_memories,
                                netName='net4',
                                densityName='learnt-' + str(Globals().greedy_run_no))
        exportData.saveToJson()
    Globals().greedy_run_no += 1
    print(f'rewards_mean:{rewards_mean} rewards_sum:{rewards_sum} cars_out:{cars_out}')
    return rewards_mean, rewards_sum, cars_out


if __name__ == "__main__":
    run_learnt_greedy()

from typing import List
from Env import Env
from env_settings import max_time
from model.Action import ActionInt
from model.ExportData import ExportData
from services.agentFactory import get_LearnSmartAgents
from services.globals import Globals


def epoch_greedy(env) -> Env:
    Globals().time = 0
    old_epsion=Globals().epsilon
    Globals().epsilon = 0
    actions_count = [0, 0]
    for t in range(max_time):
        actions: List[ActionInt] = [agent.get_action(state=agent.local_state,full_random=False) for agent in env.agents]
        actions_count[actions[0]] += 1
        env.step(actions)
    print('greedy podjęte akcje:',actions_count)
    Globals().epsilon = old_epsion
    return env

def count_rewards(env):
    memsum = 0
    i = 0
    for agent in env.agents:
        for mem in agent.memories:
            i += 1
            memsum += mem.reward
    return memsum, memsum / i


def run_learnt_greedy(saveJson=True):
    model_file_names = ['static_files/model-agent0.h5']
    agents = get_LearnSmartAgents(model_file_names)
    env = Env(agents)
    epoch_greedy(env)
    rewards_sum, rewards_mean = count_rewards(env)
    cars_out = env.cars_out
    if saveJson:
        exportData = ExportData(learningMethod='DQN', learningEpochs=0, nets=env.global_memories,
                                netName='net11',
                                densityName='learnt_' + str(Globals().greedy_run_no))
        exportData.saveToJson()
    Globals().greedy_run_no += 1
    print(f'gready run - rewards_mean:{rewards_mean} rewards_sum:{rewards_sum} cars_out:{cars_out}')
    return rewards_mean, rewards_sum, cars_out

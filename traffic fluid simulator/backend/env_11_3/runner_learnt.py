from Env import Env
from Utils import count_rewards
from model.ExportData import ExportData
from services.runnerService import epoch_greedy
from services.agentFactory import get_LearnSmartAgents
from services.globals import Globals


def run_learnt_greedy(saveJson=False):
    saveJson = True
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


if __name__ == "__main__":
    run_learnt_greedy()

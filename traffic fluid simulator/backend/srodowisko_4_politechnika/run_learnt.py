from Env import Env
from Utils import count_rewards
from model.ExportData import ExportData
from services.runnerService import epoch_greedy, run_learnt_greedy
from services.agentFactory import get_LearnSmartAgents
from services.globals import Globals

#
# def run_learnt_greedy(saveJson=True):
#     Globals().cars_out_memory = []
#     model_file_names = ['static_files/model-agent0.h5', 'static_files/model-agent1.h5', 'static_files/model-agent2.h5',
#                         'static_files/model-agent3.h5']
#     agents = get_LearnSmartAgents(model_file_names)
#     env = Env(agents)
#     u=epoch_greedy(env)
#     rewards_sum, rewards_mean = count_rewards(env)
#     cars_out = env.cars_out
#     if saveJson:
#         exportData = ExportData(learningMethod='DQN', learningEpochs=0, nets=env.global_memories,
#                                 netName='polibuda',
#                                 densityName='learnt_' + str(Globals().greedy_run_no))
#         exportData.saveToJson()
#     maximum_possible_cars_out = Globals().u_value * Globals().vp.max_time_greedy * 8
#     print(
#         f'gready run {Globals().greedy_run_no} - rewards_mean:{round(rewards_mean, 2)} rewar'
#         f'ds_sum:{round(rewards_sum, 0)}. Do układu wjechało {round(sum(sum(u)),0)} pojazdów. Wyjechało {round(cars_out, 0)}. Układ opuściło pr'
#         f'ocentowo pojazdów:{round(100*cars_out / maximum_possible_cars_out,2)}')
#     Globals().greedy_run_no += 1
#     return rewards_mean, rewards_sum, cars_out, agents,sum(sum(u))


if __name__ == "__main__":
    run_learnt_greedy()

from Env import Env
from Utils import count_rewards
from env_settings import generate_u
from model.ExportData import ExportData
from services.runnerService import epoch_greedy
from services.agentFactory import get_LearnSmartAgents
from services.globals import Globals


def run_learnt_greedy(saveJson=False):
    saveJson = True
    print('greedy')
    model_file_names = ['static_files/model-agent0.h5', 'static_files/model-agent1.h5', 'static_files/model-agent2.h5']
    agents = get_LearnSmartAgents(model_file_names)
    # print('weights!',agents[0].model.weights[0])
    env = Env(agents)
    epoch_greedy(env)
    # env.update_memory_rewards() # TODO czy to mozna odkomentowac?
    rewards_sum, rewards_mean = count_rewards(env)
    cars_out = env.cars_out
    # print('cars_out',cars_out)
    if saveJson:
        exportData = ExportData(learningMethod='DQN', learningEpochs=0, nets=env.global_memories,
                                netName='net16',
                                densityName='learnt_' + str(Globals().greedy_run_no))
        exportData.saveToJson()
    max_time = Globals().vp().max_time_greedy
    maximum_possible_cars_out=Globals().u_value*Globals().vp().max_time_greedy*3
    print('max greedy',max([max(x) for x in env.x]))
    print(
        f'gready run {Globals().greedy_run_no} - rewards_mean:{rewards_mean} rewards_sum:{rewards_sum} cars_out:{cars_out} procentowo:{float(cars_out)/maximum_possible_cars_out}')
    Globals().greedy_run_no += 1
    # a=2/0
    return rewards_mean, rewards_sum, cars_out


if __name__ == "__main__":
    run_learnt_greedy()
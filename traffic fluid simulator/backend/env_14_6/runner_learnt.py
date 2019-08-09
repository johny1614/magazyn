from Env import Env
from Utils import count_rewards
from env_settings import generate_u
from model.ExportData import ExportData
from services.runnerService import epoch_greedy
from services.agentFactory import get_LearnSmartAgents
from services.globals import Globals


def run_learnt_greedy(saveJson=False):
    saveJson = True
    model_file_names = ['static_files/model-agent0.h5']
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
                                netName='net14',
                                densityName='learnt_' + str(Globals().greedy_run_no))
        exportData.saveToJson()
    Globals().greedy_run_no += 1
    print(
        f'gready run {Globals().greedy_run_no} - rewards_mean:{rewards_mean} rewards_sum:{rewards_sum} cars_out:{cars_out}')
    isPassed = False
    if cars_out > sum(sum(env.u)) * 0.99:
        new_cars_incoming = env.u[0][0] * 1.2
        Globals().u = generate_u(new_cars_incoming)
        print('zwiekszamy u na ', new_cars_incoming)
    return rewards_mean, rewards_sum, cars_out


if __name__ == "__main__":
    run_learnt_greedy()

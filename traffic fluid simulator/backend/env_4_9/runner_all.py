from timeit import default_timer as timer
from nn_trainer import train
from random_epochs_generator import generate_random_epochs
from runner_learnt import run_learnt_greedy
import matplotlib.pyplot as plt

from services.globals import Globals

runs = [0, 1, 2]
for run in runs:
    Globals().pred_plot_memory = []
    Globals().run_no = run
    results = []
    timeToLearn = 600
    startTime = timer()
    generate_random_epochs(learntAgents=False, epochs=range(50))  # bierze nowych agentow i tu jest 'is'
    train()
    run_learnt_greedy()
    while timer() - startTime < timeToLearn:
        print('czas', timer() - startTime)
        generate_random_epochs(learntAgents=True, epochs=range(50))
        train(max_time_learn=40)
        result = run_learnt_greedy()
        results.append(result)
    # print(times)
    plt.plot([res[0] for res in results])
    plt.title('Średnia wszystkich nagród - akcje wedle wyuczonej strategii')
    plt.savefig('rewards_mean' + str(run) + '.png')
    plt.close()
    # plt.show()  # rewards_mean
    plt.plot([res[1] for res in results])
    plt.title('Suma nagród - akcje wedle wyuczonej strategii')
    plt.savefig('rewards' + str(run) + '.png')
    plt.close()
    # plt.show()  # rewards
    plt.plot([res[2] for res in results])
    plt.title('Ilość pojazdów opuszczających układ - akcje wedle wyuczonej strategii')
    plt.savefig('cars_out' + str(run) + '.png')
    plt.close()
    # plt.show()  # cars_out

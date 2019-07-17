from timeit import default_timer as timer
from nn_trainer import train
from random_epochs_generator import generate_random_epochs
from runner_learnt import run_learnt_greedy
import matplotlib.pyplot as plt
from services.agentFactory import get_LearnSmartAgents, get_SmartAgents
import numpy as np

from services.globals import Globals

def draw_predictions(no):
    agents = get_LearnSmartAgents()
    to_predict = []
    for den0 in range(60):
        for den1 in range(60):
            to_predict.append([den0*2, den1*2, 1])
    predictions = agents[0].model.predict(np.array(to_predict))  # tylko dla stanow z faza 0
    dots_action_0 = []
    dots_action_1 = []
    dots_action_orange = []
    for i in range(len(predictions)):
        pred = predictions[i]
        to_predict_state = to_predict[i]
        best_action_predicted = np.argmax(pred[:-1])
        if best_action_predicted == 0:
            dots_action_0.append(to_predict_state)
        if best_action_predicted == 1:
            dots_action_1.append(to_predict_state)
        if best_action_predicted == 2:
            dots_action_orange.append(to_predict_state)

    plt.plot([den[0] for den in dots_action_0], [den[1] for den in dots_action_0], 'go')
    plt.plot([den[0] for den in dots_action_1], [den[1] for den in dots_action_1], 'ro')
    # plt.plot([den[0] for den in dots_action_orange], [den[1] for den in dots_action_orange], 'bo')
    plt.savefig('predictions' + str(no) + '.png')
    plt.close()

runs = [0]
for run in runs:
    Globals().pred_plot_memory = []
    Globals().run_no = run
    results = []
    timeToLearn = 100
    startTime = timer()
    generate_random_epochs(learntAgents=False, epochs=range(40))  # bierze nowych agentow i tu jest 'is'
    train(learntAgents=False)
    run_learnt_greedy()
    lurns=0
    while timer() - startTime < timeToLearn:
        print('czas', timer() - startTime)
        generate_random_epochs(learntAgents=True, epochs=range(40))
        train(max_time_learn=40)
        result = run_learnt_greedy()
        print('result!',result)
        results.append(result)
        draw_predictions(lurns)
        lurns+=1


    # rewards_mean
    plt.plot([res[0] for res in results])
    plt.title('Średnia wszystkich nagród - akcje wedle wyuczonej strategii')
    plt.savefig('rewards_mean' + str(run) + '.png')
    plt.close()

    # rewards
    plt.plot([res[1] for res in results])
    plt.title('Suma nagród - akcje wedle wyuczonej strategii')
    plt.savefig('rewards' + str(run) + '.png')
    plt.close()

    # cars_out
    plt.plot([res[2] for res in results])
    plt.title('Ilość pojazdów opuszczających układ - akcje wedle wyuczonej strategii')
    plt.savefig('cars_out' + str(run) + '.png')
    plt.close()

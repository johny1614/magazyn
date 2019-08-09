from timeit import default_timer as timer
from nn_trainer import train, plot_pred_memory
from random_epochs_generator import generate_random_epochs
from runner_learnt import run_learnt_greedy
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from services.agentFactory import get_LearnSmartAgents, get_SmartAgents
import numpy as np

from services.globals import Globals

def draw_weights():
    agents = get_LearnSmartAgents()
    for agent in agents:
        agent.plot_weights()

def draw_predictions(no):
    agents = get_LearnSmartAgents()
    to_predict = []
    for den0 in range(25):
        for den1 in range(25):
            for den2 in range(25):
                for den3 in range(25):
                    to_predict.append([den0, den1, den2, den3, 1, 0, 0, 0])  # na razie dla fazy 0
    predictions = agents[0].model.predict(np.array(to_predict))
    dots_action_0 = []
    dots_action_1 = []
    dots_action_orange = []
    for i in range(len(predictions)):
        pred = predictions[i]
        to_predict_state = to_predict[i]
        best_action_predicted = np.argmax(pred)
        if best_action_predicted == 0:
            dots_action_0.append(to_predict_state)
        if best_action_predicted == 1:
            dots_action_1.append(to_predict_state)
        if best_action_predicted == 2:
            dots_action_orange.append(to_predict_state)
    # os x to den z gory os y to den z dolu
    fig, ax = plt.subplots()
    for den1 in range(25):
        for den3 in range(25):
            actions_0_better = len([den for den in dots_action_0 if den[1] == den1 and den[3] == den3])
            actions_1_better = len([den for den in dots_action_1 if den[1] == den1 and den[3] == den3])
            all = actions_0_better + actions_1_better
            if all == 0:
                ax.plot(den1, den3, 'o', color=(0, 0, 0))
                continue
            # print('action_0_better',actions_0_better)
            # print('action_1_better',actions_1_better)
            red = actions_0_better / all
            green = actions_1_better / all
            # print('red', actions_0_better)
            # print('green', actions_1_better)
            # print('r', red)
            # print('g', green)
            # if den1==den3:
            #     print(green)
            ax.plot(den1, den3, 'o', color=(red, green, 0))
    # plt.plot([den[1] for den in dots_action_0], [den[3] for den in dots_action_0], 'ro')
    # plt.plot([den[1] for den in dots_action_1], [den[3] for den in dots_action_1], 'go')
    # plt.plot([den[0] for den in dots_action_orange], [den[1] for den in dots_action_orange], 'bo')
    # print("draw pred!")
    # fig.savefig('plotcircles.png')
    name = 'predictions' + str(no) + '.png'
    fig.savefig(name)
    plt.close(fig)
    a = 3
    # fig.close()


runs = range(len(Globals().val_params))
for run in runs:
    Globals().pred_plot_memory = []
    Globals().run_no = run
    results = []
    timeToLearn = 500000
    startTime = timer()
    generate_random_epochs(learntAgents=False,
                           epochs=range(Globals().vp().first_epochs_range))  # bierze nowych agentow i tu jest 'is'
    train(learntAgents=False,max_time_learn=Globals().vp().max_time_learn)
    run_learnt_greedy()
    lurns = 0
    i = 0
    while timer() - startTime < timeToLearn:
        print('czas', timer() - startTime)
        generate_random_epochs(learntAgents=True, epochs=range(Globals().vp().epochs_range))
        train(max_time_learn=Globals().vp().max_time_learn)
        result = run_learnt_greedy()
        results.append(result)
        lurns += 1
        name = 'teraz' + str(i) + "time" + str(timer() - startTime) + " " + str(Globals().vp())
        draw_predictions(name)
        plot_pred_memory('teraz' + str(i))
        i += 1
        for i in range(len(Globals().pred_plot_memory)):
            mem = Globals().pred_plot_memory[i]
        draw_weights()
            # print(f"memory:{i} {mem}")
    #
    #
    # rewards_mean
    print(f'Run:{run}', Globals().vp())
    draw_predictions(Globals().vp())
    plot_pred_memory()
    Globals().pred_plot_memory = []

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

from timeit import default_timer as timer

from draw_batches import draw_batches, draw_colored_batches, draw_batches_from_agent
from env_settings import generate_u
from nn_trainer import train, plot_pred_memory
from random_epochs_generator import generate_random_epochs
import matplotlib.pyplot as plt
from runner_learnt import run_learnt_greedy
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
    multiplier = 8
    for den0 in range(25):
        for den1 in range(25):
            for den2 in range(25):
                for den3 in range(25):
                    to_predict.append([den0 * multiplier, den1 * multiplier, den2 * multiplier, den3 * multiplier,
                                       1, 0])  # na razie dla fazy 0 spodziewamy sie troche bardziej czerwonego wykresu
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
            actions_0_better = len(
                [den for den in dots_action_0 if den[1] == den1 * multiplier and den[3] == den3 * multiplier])
            actions_1_better = len(
                [den for den in dots_action_1 if den[1] == den1 * multiplier and den[3] == den3 * multiplier])
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


def draw_rewards_mean(results):
    plt.plot([res[0] for res in results])
    plt.title('Średnia wszystkich nagród - akcje wedle wyuczonej strategii')
    plt.savefig('plot_rewards_mean' + str(run) + '.png')
    plt.close()


def draw_rewards(results):
    plt.plot([res[1] for res in results])
    plt.title('Suma nagród - akcje wedle wyuczonej strategii')
    plt.savefig('plot_rewards' + str(run) + '.png')
    plt.close()


def draw_cars_out(results):
    plt.plot([res[2] for res in results])
    plt.title('Ilość pojazdów opuszczających układ - akcje wedle wyuczonej strategii')
    plt.savefig('plot_cars_out' + str(run) + '.png')
    plt.close()


# runs = range(len(Globals().val_params))
runs=[0]
for run in runs:
    Globals().pred_plot_memory = []
    Globals().run_no = run
    results = []
    timeToLearn = 500000
    startTime = timer()
   #  agents=generate_random_epochs(learntAgents=False,
   #                         epochs=range(Globals().vp().first_epochs_range))  # bierze nowych agentow i tu jest 'is'
   # # draw_colored_batches(agents)
   #  train(learntAgents=False, max_time_learn=Globals().vp().max_time_learn)
   #  result=run_learnt_greedy()
    lurns = 0
    eps_decay = 0
    while timer() - startTime < timeToLearn:
        eps_decay += 0.04
        Globals().epsilon = 1 - eps_decay
        if Globals().epsilon < 0.2:
            Globals().epsilon = 0.2
        print('epsilon', Globals().epsilon)
        print('czas', timer() - startTime)
        print('U', Globals().u_value)
        generate_random_epochs(learntAgents=True, epochs=range(Globals().vp().epochs_range))
        draw_batches('static_files/x_batch'+str(Globals().greedy_run_no))
        train(max_time_learn=Globals().vp().max_time_learn)
        result = run_learnt_greedy()
        draw_batches_from_agent(result[3], file_name='static_files/x_batch_greedy'+str(Globals().greedy_run_no))
        maximum_possible_cars_out = Globals().u_value*Globals().vp().max_time_greedy*8
        print('max possible',maximum_possible_cars_out)
        if result[2] >  maximum_possible_cars_out * 0.93:  # cars_out
            print('u przed',Globals().u_value)
            Globals().u_value=Globals().u_value*1.2
            # print('u po',Globals().u_value)
        results.append(result)
        lurns += 1
        name = 'teraz' + str(Globals().greedy_run_no) + "time" + str(timer() - startTime) + " " + str(Globals().vp())
        # draw_predictions(name)age
        # plot_pred_memory('teraz' + str(Globals().greedy_run_no))
        # for i in range(len(Globals().pred_plot_memory)):
        #     mem = Globals().pred_plot_memory[i]
        # draw_weights()
        draw_rewards_mean(results)
        draw_rewards(results)
        draw_cars_out(results)

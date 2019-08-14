import random
from timeit import default_timer as timer

from env_settings import generate_u
from nn_trainer import train, plot_pred_memory, get_batches
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

def random_predictions(number=10):
    agents = get_LearnSmartAgents()
    for i in range(number):
        pred=agents[0].model.predict(np.array([[random.randint(0,40) for x in range(12)]]))
        print('pred',pred)

print('start')
x_batch_history=[]
y_batch_history=[]
runs = range(len(Globals().val_params))
for run in runs:
    Globals().pred_plot_memory = []
    Globals().run_no = run
    results = []
    timeToLearn = 500000
    startTime = timer()
    generate_random_epochs(learntAgents=False,
                           epochs=range(Globals().vp().first_epochs_range))  # bierze nowych agentow i tu jest 'is'
    batches = get_batches(agents=get_SmartAgents())
    train(learntAgents=False, max_time_learn=Globals().vp().max_time_learn, batches=batches)
    Globals().x_batch_history.append(batches[0]['x_batch'])
    Globals().y_batch_history.append(batches[0]['y_batch'])
    run_learnt_greedy()
    lurns = 0
    eps_decay = 0
    while timer() - startTime < timeToLearn:
        generate_random_epochs(learntAgents=True, epochs=range(Globals().vp().epochs_range))
        batches = get_batches(agents=get_LearnSmartAgents())
        print('x_batch porownanie runner',Globals().x_batch_history[-1]==batches[0]['x_batch']) # tu jest dobrze - false
        print('y_batch porownanie runner',Globals().y_batch_history[-1]==batches[0]['y_batch']) # tu jest dobrze - false
        Globals().x_batch_history.append(batches[0]['x_batch'])
        Globals().y_batch_history.append(batches[0]['y_batch'])
        train(max_time_learn=Globals().vp().max_time_learn,batches=batches)
        result = run_learnt_greedy()
        results.append(result)
        random_predictions()
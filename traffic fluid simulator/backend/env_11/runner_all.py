from timeit import default_timer as timer
from random_epochs_generator import do_epoch
from runner_learnt import run_learnt_greedy
import matplotlib.pyplot as plt

from services.agentFactory import get_SmartAgents
from services.globals import Globals

agents = get_SmartAgents()
Globals().pred_plot_memory = []
results = {'cars_out': []}
timeToLearn = 100
startTime = timer()
while timer() < timeToLearn:
    env = do_epoch(agents)
    print(f'cars_out:{env.cars_out} epsilon:{Globals().epsilon}')
    results['cars_out'].append(env.cars_out)
    for agent in agents:
        agent.count_G()
        agent.count_Q()
        agent.count_PI()
        Globals().epsilon = Globals().epsilon * 0.99
        # Globals().epsilon = Globals().epsilon * 1
    draw_data_0 = []
    draw_data_1 = []
    draw_data_orange = []
    # plotting for phase 0
    for sa in agents[0].Pi:
        if len(sa) == 3 and sa[2] == 0:
            first_section = sa[0]
            second_section = sa[1]
            action = agents[0].Pi
            if action == 0:
                draw_data_0.append([first_section, second_section])
            elif action == 1:
                draw_data_1.append([first_section, second_section])
            else:
                draw_data_orange.append([first_section, second_section])
plt.plot([data[0] for data in draw_data_0], [data[1] for data in draw_data_0], 'ro')
plt.plot([data[0] for data in draw_data_1], [data[1] for data in draw_data_1], 'go')
# plt.plot([data[0] for data in draw_data_orange], [data[1] for data in draw_data_orange], 'bo')
# plt.axis([0, 6, 0, 20])
plt.show()
a=4
# plt.plot(results['cars_out'])
# plt.title('Ilość pojazdów opuszczających układ - akcje wedle wyuczonej strategii')
# plt.savefig('cars_out' + str(0) + '.png')
# plt.close()

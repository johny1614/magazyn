from timeit import default_timer as timer
from nn_trainer import train
from services.drawerService import draw_rewards_mean, draw_rewards, draw_cars_out, draw_cars_out_percentage, draw_max
from services.globals import Globals
from services.runnerService import generate_random_epochs, run_learnt_greedy

results = []
timeToLearn = 500000
startTime = timer()
agents = generate_random_epochs(learntAgents=False,
                                epochs=range(Globals().vp.first_epochs_range))  # bierze nowych agentow i tu jest 'is'
train(learntAgents=False, max_time_learn=Globals().vp.max_time_learn)
result = run_learnt_greedy()
eps_decay = 0
max_iterations_without_progress = 20
iterations_without_progress = 0
while timer() - startTime < timeToLearn:
    eps_decay += 0.04
    Globals().epsilon = 1 - eps_decay
    if Globals().epsilon < 0.2:
        Globals().epsilon = 0.2
    print(
        f'Czas:{round(timer() - startTime, 0)} Epsilon:{round(Globals().epsilon, 2)} Średnia liczba wjeżdżających pojazdów:'
        f':{round(Globals().u_value, 2)}')
    generate_random_epochs(learntAgents=True, epochs=range(Globals().vp.epochs_range))
    train(max_time_learn=Globals().vp.max_time_learn)
    result = run_learnt_greedy()
    maximum_possible_cars_out = result[4]
    if result[2] > maximum_possible_cars_out * 0.93:  # cars_out
        Globals().u_value = Globals().u_value * 1.2
        iterations_without_progress = 0
    else:
        iterations_without_progress += 1
        if iterations_without_progress == max_iterations_without_progress:
            exit()
    results.append(result)
    draw_cars_out_percentage(results)
    draw_rewards_mean(results)
    draw_rewards(results)
    draw_cars_out(results)
    draw_max(results)

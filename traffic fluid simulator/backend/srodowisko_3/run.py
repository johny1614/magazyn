from timeit import default_timer as timer
from nn_trainer import train
from services.drawerService import draw_rewards_mean, draw_cars_out
from services.globals import Globals
from services.runnerService import run_learnt_greedy, generate_random_epochs

Globals().pred_plot_memory = []
Globals().run_no = 0
results = []
timeToLearn = 500000
startTime = timer()
agents = generate_random_epochs(learntAgents=False,
                       epochs=range(Globals().vp().first_epochs_range))  # bierze nowych agentow i tu jest 'is'
train(learntAgents=False, max_time_learn=Globals().vp().max_time_learn)
result = run_learnt_greedy()
lurns = 0
eps_decay = 0
lurns_without_progress=0
max_lurns_without_progress = 10
while timer() - startTime < timeToLearn:
    eps_decay += 0.04
    Globals().epsilon = 1 - eps_decay
    if Globals().epsilon < 0.2:
        Globals().epsilon = 0.2
    print(f'Czas:{round(timer() - startTime, 0)} Epsilon:{round(Globals().epsilon,2)} Pojazdów wjeżdżających:{round(Globals().u_value, 2)}')
    generate_random_epochs(learntAgents=True, epochs=range(Globals().vp().epochs_range))
    train(max_time_learn=Globals().vp().max_time_learn)
    result = run_learnt_greedy()
    maximum_possible_cars_out = Globals().u_value*Globals().vp().max_time_greedy*3
    if result[2] >  maximum_possible_cars_out * 0.93:  # cars_out
        Globals().u_value=Globals().u_value*1.2
        max_lurns_without_progress = 0
    else:
        max_lurns_without_progress += 1
        if lurns_without_progress >= max_lurns_without_progress:
            print('Warunek stopu!')
            exit()
    results.append(result)
    lurns += 1
    draw_rewards_mean(results)
    draw_cars_out(results)

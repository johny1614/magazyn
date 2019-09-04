from timeit import default_timer as timer
from env_settings import generate_u
from services.nn_trainer import train
from services.drawerService import draw_cars_out, plot_pred_memory
from services.globals import Globals
from services.runnerService import run_learnt_greedy, generate_random_epochs

results = []
startTime = timer()
generate_random_epochs(learntAgents=False,
                       epochs=range(Globals().vp.epochs_range))
train(learntAgents=False, max_time_learn=Globals().vp.max_time_learn)
run_learnt_greedy()
eps_decay = 0
lurns_without_progress=0
max_lurns_without_progress=10
while True:
    eps_decay += 0.01
    Globals().epsilon = 1 - eps_decay
    if Globals().epsilon < 0.2:
        Globals().epsilon = 0.2
    print(f'Czas:{round(timer() - startTime,0)} Epsilon:{round(Globals().epsilon,2)} Pojazdów wjeżdżających:{round(Globals().u[0][0],2)}')
    generate_random_epochs(learntAgents=True, epochs=range(Globals().vp.epochs_range))
    train(max_time_learn=Globals().vp.max_time_learn)
    result = run_learnt_greedy()
    if result[2] > sum(sum(Globals().u)) * 0.98:  # cars_out
        new_cars_incoming = Globals().u[0][0] * 1.2
        Globals().u = generate_u(new_cars_incoming)
        lurns_without_progress=0
    else:
        max_lurns_without_progress+=1
        if lurns_without_progress >= max_lurns_without_progress:
            print('Warunek stopu!')
            exit()
    results.append(result)
    plot_pred_memory(str(Globals().greedy_run_no))
    for i in range(len(Globals().pred_plot_memory)):
        mem = Globals().pred_plot_memory[i]
    draw_cars_out(results,Globals().greedy_run_no)

from timeit import default_timer as timer
from nn_trainer import train
from random_epochs_generator import generate_random_epochs
from services.globals import Globals
from services.runnerService import run_learnt_greedy

Globals().pred_plot_memory = []
results = []
timeToLearn = 60
startTime = timer()
generate_random_epochs(learntAgents=False, epochs=range(50))
train(learntAgents=False)
run_learnt_greedy()
while timer() - startTime < timeToLearn:
    print('czas', timer() - startTime)
    generate_random_epochs(learntAgents=True, epochs=range(50))
    train(max_time_learn=30)
    result = run_learnt_greedy()
    results.append(result)

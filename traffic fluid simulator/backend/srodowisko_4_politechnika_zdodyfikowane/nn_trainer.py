from timeit import default_timer as timer
import numpy as np
from tensorflow.keras.optimizers import Adam
from tensorflow.python.keras.layers import Dense, Activation
from tensorflow.python.keras.models import Sequential

from services.agentFactory import get_LearnSmartAgents, get_SmartAgents
from services.globals import Globals


def get_batches(agents, actual_number=''):
    batches = []
    for i in range(len(agents)):
        filename = 'static_files/x_batch_agent_' + str(i) + '_' + str(actual_number) + '.txt'
        x_batch = np.array(np.loadtxt(filename, delimiter=','))
        filename = 'static_files/y_batch_agent_' + str(i) + '_' + str(actual_number) + '.txt'
        y_batch = np.array(np.loadtxt(filename, delimiter=','))
        batches.append({'x_batch': x_batch, 'y_batch': y_batch})
    return batches


def train(learntAgents=True, max_time_learn=60, agents=None, batches=None, actual_number=''):
    if agents is None:
        if not learntAgents:
            agents = get_SmartAgents()
        else:
            agents = get_LearnSmartAgents()
    if batches is None:
        batches = get_batches(agents, actual_number)
    models = [agent.model for agent in agents]
    for i in range(len(agents)):
        start_time = timer()
        x_batch = batches[i]['x_batch']
        y_batch = batches[i]['y_batch']
        model = models[i]
        weights_best = model.get_weights()
        val_loss = 10 ** 10
        val_loss_best = 10 ** 10
        escape_flag = False
        escape_val = 0
        start_flag = True
        while timer() - start_time < max_time_learn and not escape_flag:
            res = model.fit(x_batch, y_batch, batch_size=Globals().vp.batch_size,
                            initial_epoch=Globals().epochs_learn_done,
                            epochs=Globals().epochs_learn_done + Globals().vp.epochs_learn,
                            validation_split=0.2,
                            verbose=0)
            Globals().epochs_learn_done += Globals().vp.epochs_learn
            if start_flag:
                start_flag = False
            if res.history['val_loss'][-1] < val_loss_best:
                val_loss_best = res.history['val_loss'][-1]
                weights_best = model.get_weights()
            if res.history['val_loss'][-1] >= val_loss:
                escape_val += 1
                if escape_val > 10:
                    escape_flag = True
                val_loss = 10 ** 10
            else:
                val_loss = res.history['val_loss'][-1]
        print('loss',val_loss_best)
        model.set_weights(weights_best)
        model.save('static_files/model-agent' + str(i) + '.h5')

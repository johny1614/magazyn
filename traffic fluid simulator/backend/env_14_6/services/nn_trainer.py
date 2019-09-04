from timeit import default_timer as timer
import numpy as np
from tensorflow.keras.optimizers import Adam
from tensorflow.python.keras.layers import Dense, Activation
from tensorflow.python.keras.models import Sequential

from services.agentFactory import get_LearnSmartAgents, get_SmartAgents
from services.globals import Globals


def get_batches():
    batches = []
    for i in range(1):
        filename = 'static_files/x_batch_agent_' + str(i) + '.txt'
        x_batch = np.array(np.loadtxt(filename, delimiter=','))
        filename = 'static_files/y_batch_agent_' + str(i) + '.txt'
        y_batch = np.array(np.loadtxt(filename, delimiter=','))
        batches.append({'x_batch': x_batch, 'y_batch': y_batch})
    return batches


def train(learntAgents=True, max_time_learn=60, agents=None):
    if agents is None:
        if not learntAgents:
            agents = get_SmartAgents()
        else:
            agents = get_LearnSmartAgents()
    models = [agent.model for agent in agents]
    batches = get_batches()
    for i in range(1):
        start_time = timer()
        x_batch = batches[i]['x_batch']
        y_batch = batches[i]['y_batch']
        model = models[i]
        weights_best = model.get_weights()
        val_loss = 10 ** 10
        val_loss_best = 10 ** 10
        escape_flag = False
        escape_val = 0
        while timer() - start_time < max_time_learn and not escape_flag:
            res = model.fit(x_batch, y_batch, batch_size=Globals().vp.batch_size,
                            initial_epoch=Globals().epochs_done,
                            epochs=Globals().epochs_done + Globals().epochs_learn,
                            validation_split=0.2,
                            verbose=0)  # callbacks=[Globals().tensorboard,agents[i].weights_history_callback]
            Globals().epochs_done += Globals().epochs_learn
            if res.history['val_loss'][-1] < val_loss_best:
                val_loss_best = res.history['val_loss'][-1]
                weights_best = model.get_weights()
            if res.history['val_loss'][-1] > val_loss:
                escape_val += 1
                if escape_val > 2:
                    escape_flag = True
                val_loss = 10 ** 10
            else:
                val_loss = res.history['val_loss'][-1]
            if i == 0:
                x = [0, 0, 10, 15, 1, 0]  # dla fazy 0 - lepiej jednak jakby zmienil na swiatlo 1
                pred = model.predict(np.array([x]))
                Globals().pred_plot_memory.append(pred)
        model.set_weights(weights_best)
        model.save('static_files/model-agent' + str(i) + '.h5')


if __name__ == "__main__":
    train()

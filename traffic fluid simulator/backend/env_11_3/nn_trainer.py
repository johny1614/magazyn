from timeit import default_timer as timer

import matplotlib.pyplot as plt
import numpy as np

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


def train(learntAgents=True, max_time_learn=20):
    if not learntAgents:
        agents = get_SmartAgents()
    else:
        agents = get_LearnSmartAgents()
    models = [agent.model for agent in agents]
    batches = get_batches()
    start_time = timer()
    x_batch = batches[0]['x_batch']
    y_batch = batches[0]['y_batch']
    model = models[0]
    val_loss = 5000
    escape_flag = False
    while timer() - start_time < max_time_learn and not escape_flag:
        res = model.fit(x_batch, y_batch, batch_size=100, epochs=1, verbose=0, validation_split=0.2)
        if res.history['val_loss'][-1] > val_loss:
            escape_flag = True
            loss = res.history['val_loss'][-1]
            print(f'wynik sieci: {loss} straty')
            val_loss = 5000
        else:
            val_loss = res.history['val_loss'][-1]
        x = [4, 20]
        pred = model.predict(np.array([x]))
        Globals().pred_plot_memory.append(pred)
    model.save('static_files/model-agent' + str(0) + '.h5')
    plt.plot([pred[0][0] for pred in Globals().pred_plot_memory], color='red', label='0')
    plt.plot([pred[0][1] for pred in Globals().pred_plot_memory], color='green', label='1')
    plt.legend()
    plt.title('Nagrody przewidziane dla akcji podjętych \n podczas monitorowanego stanu [4, 20]')
    plt.savefig('images_generated/state_predictions.png')
    plt.close()


if __name__ == "__main__":
    train()

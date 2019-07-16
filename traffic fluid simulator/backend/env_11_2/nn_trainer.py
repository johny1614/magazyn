from timeit import default_timer as timer

import matplotlib.pyplot as plt
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


def create_model(layers, activation, l_rate):
    model = Sequential()
    for i, nodes in enumerate(layers):
        if i == 0:
            model.add(Dense(nodes, input_dim=10, activation='linear'))
        else:
            model.add(Dense(nodes))
            model.add(Activation(activation))
    model.add(Dense(3))  # Note: no activation beyond this point
    model.compile(optimizer=Adam(learning_rate=l_rate), loss='mse')
    return model


def train(learntAgents=True, max_time_learn=20):
    if not learntAgents:
        agents = get_SmartAgents()
    else:
        print('get learnt!')
        agents = get_LearnSmartAgents()
        a=7
    models = [agent.model for agent in agents]
    batches = get_batches()
    for i in range(1):
        start_time = timer()
        x_batch = batches[i]['x_batch']
        y_batch = batches[i]['y_batch']
        model = models[i]
        val_loss = 5000
        escape_flag = False
        while timer() - start_time < max_time_learn and not escape_flag:
            res = model.fit(x_batch, y_batch, batch_size=100, epochs=1, verbose=0, validation_split=0.2)
            if res.history['val_loss'][-1] > val_loss:
                escape_flag = True
                print('wynik sieci', res.history['val_loss'][-1])
                val_loss = 5000
            else:
                val_loss = res.history['val_loss'][-1]
            if i == 0:
                x = [4, 40, 0]
                pred = model.predict(np.array([x]))
                Globals().pred_plot_memory.append(pred)
        model.save('static_files/model-agent' + str(i) + '.h5')
        if i == 0:
            plt.plot([pred[0][0] for pred in Globals().pred_plot_memory], color='red', label='0')
            plt.plot([pred[0][1] for pred in Globals().pred_plot_memory], color='green', label='1')
            plt.plot([pred[0][2] for pred in Globals().pred_plot_memory], color='blue', label='2')
            plt.legend()
            plt.title('Nagrody przewidziane dla akcji podjętych podczas monitorowanego stanu')
            plt.savefig('foo' + str(Globals().run_no) + '.png')
            plt.close()


if __name__ == "__main__":
    train()
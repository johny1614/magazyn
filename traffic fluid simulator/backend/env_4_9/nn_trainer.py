import numpy as np
import matplotlib.pyplot as plt
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.activations import sigmoid, relu
from tensorflow.python.keras.layers import Dense, Activation, BatchNormalization
from tensorflow.python.keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import GridSearchCV
from timeit import default_timer as timer
from tensorflow.keras.optimizers import Adam
from tensorflow.python.keras import regularizers

from services.agentFactory import get_LearnSmartAgents
from services.globals import Globals


def get_batches():
    batches = []
    for i in range(3):
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
    l_rate = 0.0001
    layers = [15, 25, 20, 15]
    optimizer = 'relu'
    regularizers_ = [0.2, 0.2, 0.2]
    print('train learntAgents', learntAgents)
    agents = get_LearnSmartAgents()

    # create_model(layers, optimizer, l_rate)
    # for i in range(3)
    models = [agent.model for agent in agents]
    batches = get_batches()
    # for i in range(len(models)):
    for i in range(3):
        start_time = timer()
        x_batch = batches[i]['x_batch']
        y_batch = batches[i]['y_batch']
        model = models[i]
        x2 = []
        y2 = []
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
            # res = model.fit(np.array(x2), np.array(y2), batch_size=20, epochs=1, verbose=0)
            if i == 0:
                # x = [7, 10, 10] + [10, 10, 20] + [6, 5, 4] + [2]
                x = [4, 4, 62] + [10, 10, 49] + [ 0, 10, 10] + [0]
                pred = model.predict(np.array([x]))
                Globals().pred_plot_memory.append(pred)
            # model.evaluate(np.array(x2), np.array(y2))
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

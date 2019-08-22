from operator import itemgetter
import time
import matplotlib.pyplot as plt

import numpy as np
from tensorflow.python.keras.callbacks import TensorBoard
from tensorflow.keras.optimizers import Adam
from tensorflow.python.keras.layers import Dense, Activation
from tensorflow.python.keras.models import Sequential
import random
import tensorflow as tf
from tensorflow.python.keras.utils.vis_utils import plot_model


def _build_model(hidden_layers, activation='relu', l_rate=0.01):
    model = Sequential()
    for i, nodes in enumerate(hidden_layers):
        if i == 0:
            model.add(Dense(nodes, input_dim=1, activation='linear'))
        else:
            model.add(Dense(nodes))
            model.add(Activation(activation))
    model.add(Dense(1))
    model.compile(optimizer=Adam(learning_rate=l_rate), loss='mse')
    return model


def weight_log_handler(epoch, logs):
    weights = model.get_weights()
    weights_history.append(weights)
    if epoch % 100 == 0:
        print('epoch', epoch)
        print('weights', weights)
        model.evaluate(x, y)
        # weights[0][0][0] = 0
        # weights[0][0][1] = 1
        # weights[1][0] = 2
        # weights[1][1] = 3
        # weights[2][0][0] = 4
        # weights[2][0][1] = 5
        # weights[2][1][0] = 6
        # weights[2][1][1] = 7
        # weights[3][0] = 8
        # weights[3][1] = 9
        # weights[4][0][0] = 10
        # weights[4][1][0] = 11
        # weights[5][0] = 12
        # model.set_weights(weights)
        a = 4
        plot_weights()


def plot_weights():
    # print('done',Globals().epochs_done)
    layers = range(len(weights_history[0]) - 1)
    bias_layers = []
    a_layers = []
    for layer in layers:
        if len(weights_history[0][layer].shape) == 2:
            a_layers.append(layer)
        if len(weights_history[0][layer].shape) == 1:
            bias_layers.append(layer)
    for bias_layer in bias_layers:
        neurons = range(len(weights_history[0][bias_layer]))
        for n in neurons:
            color = [1 - n / len(neurons), n / len(neurons), 0]
            plt.plot([x[bias_layer][n] for x in weights_history], color=color, label=str(n))
        name = 'weights_layer_' + str(bias_layer) + '.png'
        plt.savefig(name)
        plt.close()
    node = 0
    for a_layer in a_layers:
        draw = 0
        previous_nodes = range(len(weights_history[0][a_layer]))
        layer_nodes = range(len(weights_history[0][a_layer][0]))
        all_weights = len(previous_nodes) * len(layer_nodes)
        max_nodes = 15
        for prev_node in previous_nodes:
            for layer_node in layer_nodes:
                color = [1 - node / max_nodes, node / max_nodes, 0]
                plt.plot([x[a_layer][prev_node][layer_node] for x in weights_history], color=color, label=str(n))
                node += 1
                if node > max_nodes:
                    node = 0
                    # print('node',node)
                    # print('draw',draw)
                    plt.savefig(name)
                    plt.close()
                    draw += 1
        name = 'weights_layer_' + str(a_layer) + '_draw_' + str(draw) + '.png'
        plt.savefig(name)
        plt.close()


weights_history = []
l_rate = 0.001
x = np.array([[0.1 * i - 6.0] for i in range(100)])
y = np.array([3 * el ** 2 - 2 * el + 5 for el in x])
epochs = 10000000
# tb_log = tf.keras.callbacks.TensorBoard(log_dir='graph', histogram_freq=0,
#                                         write_graph=True, write_images=True)
weight_log = tf.keras.callbacks.LambdaCallback(on_epoch_end=weight_log_handler)
model = Sequential([
    Dense(8, activation='relu', name='hidden_layer1', input_shape=(1,)),
    Dense(15, activation='relu', name='hidden_layer2'),
    Dense(5, activation='relu', name='hidden_layer3'),
    Dense(1, name='output_layer'),
])
# model=Sequential()
# model.add(Dense(5,activation='relu',input_shape=(1,)))
# model.add(Dense(1,activation='relu'))
# plot_model(model, to_file='model.png', show_shapes=True)
model.compile(optimizer=Adam(), loss='mse')
res = model.fit(x, y, epochs=epochs, verbose=0, callbacks=[weight_log])
# model.summary()
# weights = model.get_weights()
a = 2

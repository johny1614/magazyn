from operator import itemgetter
import time


import numpy as np
from tensorflow.python.keras.callbacks import TensorBoard
from tensorflow.keras.optimizers import Adam
from tensorflow.python.keras.layers import Dense, Activation
from tensorflow.python.keras.models import Sequential
import random
import tensorflow as tf


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



l_rate = 0.001
x = np.array([[0.1 * i] for i in range(10)])
y = np.array([el ** 2 - 2 * el + 5 for el in x])
epochs = 100
tb_log = tf.keras.callbacks.TensorBoard(log_dir='graph', histogram_freq=0,
                            write_graph=True, write_images=True)
model = Sequential([
  Dense(4, activation='relu',name='hidden_layer1'),
  Dense(7, activation='relu',name='hidden_layer2'),
])
model.compile(optimizer=Adam(),loss='mse')
res = model.fit(x, y, epochs=epochs, verbose=1,callbacks=[tb_log])
weights = model.get_weights()
a = 2

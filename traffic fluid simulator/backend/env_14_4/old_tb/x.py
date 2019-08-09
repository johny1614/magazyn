from operator import itemgetter
import time

import numpy as np
from tensorflow.python.keras.callbacks import TensorBoard
from tensorflow.keras.optimizers import Adam
from tensorflow.python.keras.layers import Dense, Activation
from tensorflow.python.keras.models import Sequential
import random
import tensorflow as tf


def _build_model(layers, activation='relu', l_rate=0.01):
    model = Sequential()
    for i, nodes in enumerate(layers):
        if i == 0:
            model.add(Dense(nodes, input_dim=1, activation='linear'))
        else:
            model.add(Dense(nodes))
            model.add(Activation(activation))
    model.add(Dense(1))
    model.compile(optimizer=Adam(learning_rate=l_rate), loss='mse')
    return model


# layers_s=[np.random.random_integers(0,20,4) for i in range(10)]+[[10,15,22]]
layers_s = [[17, 12, 11, 13]]
l_rates = [0.001]
# layers_s=[[10,15,22],[16,5,19],[1,20,18]]
x = np.array([[0.1 * i] for i in range(400)])
y = np.array([el ** 3 + 7 * el ** 2 - 2 * el + 7 for el in x])
# layers_s = [[10,15,22]]
# [10,15,22]
scores = []
epochs = 100
i = 0
for layers in layers_s:
    for l_rate in l_rates:
        name = "X-learn-{} epochs - {}".format(int(time.time()), l_rate, epochs)
        tensorboard = TensorBoard(log_dir="logs\{}".format(name),histogram_freq=1)
        # keras.callbacks.TensorBoard(log_dir='./Graph', histogram_freq=0,
        #                             write_graph=True, write_images=True)
        print(i)
        i += 1
        model = _build_model(layers=layers, l_rate=l_rate)
        # while True:
        res = model.fit(x, y, epochs=epochs, verbose=1, callbacks=[tensorboard], validation_split=0.2)
        # print('wyliczony',sum((model.predict(x) - y)**2)/len(x))
        # print('layers',layers)
        score = res.history['loss'][-1]
        highest_score = min(res.history['loss'])
        # print('res',res.history['loss'][-1])
        # print('========')
        scores.append({'layers': layers, 'l_rate': l_rate, 'score': score, 'highest_score': highest_score})
sortedScores = sorted(scores, key=itemgetter('score'))
a = 0

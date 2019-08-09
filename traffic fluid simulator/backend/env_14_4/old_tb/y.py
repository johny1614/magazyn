from operator import itemgetter
import time

import numpy as np
from tensorflow.python.keras.callbacks import TensorBoard
from tensorflow.keras.optimizers import Adam
from tensorflow.python.keras.layers import Dense, Activation
from tensorflow.python.keras.models import Sequential
import tensorflow as tf
import random


def _build_model(neuron_num,l_rate,layer_num,activation='relu'):
    model = Sequential()
    model.add(Dense(neuron_num, input_dim=1, activation='linear'))
    for layer in range(layer_num-1):
        model.add(Dense(neuron_num))
        model.add(Activation(activation))
    model.add(Dense(1,name='koniec'))
    model.compile(optimizer=Adam(learning_rate=l_rate), loss='mse')
    return model


# layers_s=[np.random.random_integers(0,20,4) for i in range(10)]+[[10,15,22]]
neurons = [16, 32]
layers = [5, 2]
l_rates = [0.1, 0.001]
# layers_s=[[10,15,22],[16,5,19],[1,20,18]]
# print(layers_s)
# print(layer)
x = np.array([[0.1 * i] for i in range(400)])
y = np.array([el ** 3 + 7 * el ** 2 - 2 * el + 7 for el in x])
# layers_s = [[10,15,22]]
# [10,15,22]
scores = []
epochs = 100
i = 0
tf.reset_default_graph()
sess = tf.Session()
for neuron_num in neurons[:1]:
    for l_rate in l_rates[:1]:
        for layer_num in layers[:1]:
            name = "neurons_num {} l_rate {} layer_num {} time {}".format(neuron_num, l_rate, layer_num,int(time.time()))
            tensorboard = TensorBoard(log_dir="ylogs\{}".format(name))
            print('zrobiony',i)
            i += 1
            model = _build_model(neuron_num,l_rate,layer_num)
            # while True:
            res = model.fit(x, y, epochs=epochs, verbose=0, callbacks=[tensorboard], validation_split=0.2)
            # print('wyliczony',sum((model.predict(x) - y)**2)/len(x))
            # print('layers',layers)
            score = res.history['loss'][-1]
            highest_score = min(res.history['loss'])
            # print('res',res.history['loss'][-1])
            # print('========')
            scores.append({'layers': layers, 'l_rate': l_rate, 'score': score, 'highest_score': highest_score})
            sess.run(tf.global_variables_initializer())
            writer = tf.compat.v1.summary.FileWriter('ylogs')
            writer.add_su(sess.graph)
            for i, layer in enumerate(layers):
                tf.summary.histogram('layer{0}'.format(i), layer)
            merged = tf.summary.merge_all()
            writer = tf.summary.FileWriter('ylogs', sess.graph)

sortedScores = sorted(scores, key=itemgetter('score'))
a = 0

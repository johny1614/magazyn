from timeit import default_timer as timer

import numpy as np
from tensorflow.keras.optimizers import Adam
from tensorflow.python.keras.layers import Dense, Activation
from tensorflow.python.keras.models import Sequential


def create_model(layers, activation):
    model = Sequential()
    for i, nodes in enumerate(layers):
        if i == 0:
            model.add(Dense(nodes, input_dim=10, activation='linear'))
        else:
            model.add(Dense(nodes))
            model.add(Activation(activation))
    model.add(Dense(4))
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
    return model


time = timer()
x_batch = np.array(np.loadtxt('static_files/x_batch.txt', delimiter=','))
y_batch = np.array(np.loadtxt('static_files/y_batch.txt', delimiter=','))
layerss = [[20, 50, 40, 20], [30, 20, 50, 40], [30, 30, 30], [15, 20, 30, 24, 20, 12], [15, 18, 25, 10]]
learning_rates = [0.01, 0.001, 0.0001, 0.00001]
batch_sizes = [20, 50, 100, 200, 400, 600]
memories = []
for layers in layerss:
    for l_rate in learning_rates:
        for batch_size in batch_sizes:
            model = create_model(layers, 'relu')
            model.learning_rate = l_rate
            start_time = timer()
            while timer() - start_time < 5:
                res = model.fit(x_batch, y_batch, batch_size=200, epochs=50, verbose=0, validation_split=0.2)
            memory = {'l_rate': l_rate, 'layers': layers, 'val_loss': res.history['val_loss'][-1]}
            memories.append(memory)
print(memories)
print('done')

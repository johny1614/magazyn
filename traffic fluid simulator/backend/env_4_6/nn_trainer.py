import numpy as np
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.activations import sigmoid, relu
from tensorflow.python.keras.layers import Dense, Activation, BatchNormalization
from tensorflow.python.keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import GridSearchCV
from timeit import default_timer as timer
from tensorflow.keras.optimizers import Adam


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
    model.add(Dense(4))  # Note: no activation beyond this point
    model.compile(optimizer=Adam(learning_rate=l_rate), loss='mse')
    return model


l_rate = 0.00001
layers = [15, 20, 15]
optimizer = 'relu'
models = [create_model(layers, optimizer, l_rate) for i in range(3)]
batches=get_batches()
for i in range(len(models)):
    start_time = timer()
    x_batch=batches[i]['x_batch']
    y_batch=batches[i]['y_batch']
    model = models[i]
    while timer() - start_time:
        x = [0, 0, 20] + [0, 0, 0] + [0, 0, 0] + [1]
        res = model.fit(x_batch, y_batch, batch_size=300, epochs=1, verbose=1)
        print(model.predict(np.array([x])))
    model.save('model-agent' + str(i) + '.h5')

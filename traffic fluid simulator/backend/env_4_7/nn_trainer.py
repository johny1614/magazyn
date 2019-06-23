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
l_rate = 0.0001
layers = [15, 25, 20, 15]
optimizer = 'relu'
regularizers_ = [0.2, 0.2, 0.2]

models = [create_model(layers, optimizer, l_rate) for i in range(3)]
batches = get_batches()
# for i in range(len(models)):
for i in range(3):
    start_time = timer()
    x_batch = batches[i]['x_batch']
    y_batch = batches[i]['y_batch']
    model = models[i]
    model.layers[0].kernel_regularizer = regularizers.l2(regularizers_[0])
    model.layers[1].kernel_regularizer = regularizers.l2(regularizers_[1])
    model.layers[3].kernel_regularizer = regularizers.l2(regularizers_[2])
    x2 = []
    y2 = []
    preds = []
    val_loss = 5000
    escape_flag=False
    while timer() - start_time < 300 and not escape_flag:
        x = [2, 2, 2] + [10, 20, 20] + [0, 0, 0] + [1]
        res = model.fit(x_batch, y_batch, batch_size=100, epochs=1, verbose=0, validation_split=0.2)
        if res.history['val_loss'][-1] > val_loss:
            escape_flag=True
            print('koniec!',res.history['val_loss'][-1])
            val_loss=5000
        else:
            val_loss=res.history['val_loss'][-1]
        # res = model.fit(np.array(x2), np.array(y2), batch_size=20, epochs=1, verbose=0)
        # pred = model.predict(np.array([x]))
        # preds.append(pred[0])
        # print(pred)
        s=2
        # model.evaluate(np.array(x2), np.array(y2))
    model.save('static_files/model-agent' + str(i) + '.h5')
    # plt.plot([pred[0] for pred in preds], color='red')
    # plt.plot([pred[1] for pred in preds], color='green')
    # plt.plot([pred[2] for pred in preds], color='blue')
    # plt.show()
    a = 1
    # agents[i]

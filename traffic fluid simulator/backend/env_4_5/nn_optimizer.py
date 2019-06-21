import numpy as np
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.activations import sigmoid, relu
from tensorflow.python.keras.layers import Dense, Activation, BatchNormalization
from tensorflow.python.keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import GridSearchCV
from timeit import default_timer as timer
from tensorflow.keras.optimizers import Adam


def create_model(layers, activation):
    model = Sequential()
    for i, nodes in enumerate(layers):
        if i == 0:
            model.add(Dense(nodes, input_dim=10, activation='linear'))
        else:
            model.add(Dense(nodes))
            model.add(Activation(activation))
    model.add(Dense(4))  # Note: no activation beyond this point

    model.compile(optimizer='adadelta', loss='mse')
    return model


time = timer()
x_batch = np.array(np.loadtxt('x_batch.txt', delimiter=','))
y_batch = np.array(np.loadtxt('y_batch.txt', delimiter=','))

# best_model = create_model([70, 100, 150, 100, 80, 60, 30], relu)
best_model = Sequential()
best_model.add(Dense(20, input_dim=10, activation='relu'))  # 1st hidden layer; states as input
best_model.add(Dense(50, activation='relu'))
best_model.add(Dense(40, activation='relu'))
best_model.add(Dense(20, activation='relu'))
best_model.add(Dense(4, activation='linear'))
best_model.compile(loss='mse',
              optimizer=Adam(learning_rate=0.001))
i = 0
val_loss = 99999999
while True:
    i += 100
    res = best_model.fit(x_batch, y_batch, batch_size=200,epochs=50, verbose=0)
    print(res.history['loss'][-1])
    if i % 1000 == 0:
        best_model.save('here')
    # if i % 500 == 0:
    #     best_model.evaluate(x_batch,y_batch)

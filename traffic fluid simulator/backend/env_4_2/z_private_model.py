import numpy as np
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.activations import sigmoid, relu
from tensorflow.python.keras.layers import Dense, Activation, BatchNormalization
from tensorflow.python.keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import GridSearchCV
from timeit import default_timer as timer


def create_model(layers, activation):
    # global a
    # print('x',a)
    # a+=1
    model = Sequential()
    for i, nodes in enumerate(layers):
        if i == 0:
            model.add(Dense(nodes, input_dim=37, activation='linear'))
        else:
            model.add(Dense(nodes))
            model.add(Activation(activation))
    model.add(Dense(4))  # Note: no activation beyond this point

    model.compile(optimizer='adadelta', loss='mse')
    return model


time = timer()
x_batch = np.array(np.loadtxt('x_batch.txt', delimiter=','))
y_batch = np.array(np.loadtxt('y_batch.txt', delimiter=','))

# model = KerasRegressor(build_fn=create_model, verbose=0)
# layers = [[70,120], [50,100,150,100,80,60,30]]
# # layers = [[70,120], [45, 60, 90],[30,10],[50,70],[20,50,70,40],[30,20,40,20],[70,120,70],[50,100,150,100,80,60,30]]
# activations = [relu]
# param_grid = dict(layers=layers, activation=activations, batch_size = [128, 256], epochs=[700])
# a=1
# grid = GridSearchCV(estimator=model, param_grid=param_grid, scoring='neg_mean_squared_error')
# # print(len(x_batch))
# grid_result = grid.fit(x_batch[0:2000], y_batch[0:2000])

# best_model = create_model([45, 60, 90], relu)

best_model = create_model([70, 100, 150, 100, 80, 60, 30], relu)
# best_model.fit(x_batch,y_batch,epochs=1700,validation_split=0.2)
i = 0
val_loss = 99999999
while True:
    print('epoch:' + str(i))
    i += 200
    res = best_model.fit(x_batch, y_batch, validation_split=0.2, epochs=100, verbose=0)
    # print('loss',res.history['val_loss'][-1])
    # print(f"loss {res.history['loss'][-1]} val_loss: {res.history['val_loss'][-1]}")
    # if res.history['val_loss'][-1] > val_loss:
    #     print('KONIEC!')
    #     break
    # val_loss = res.history['val_loss'][-1]
    # print(val_loss)
    # print(res.history['loss'][-1])

# best_model=create_model(grid_result.best_params_['layers'],relu)
# print([grid_result.best_score_, grid_result.best_params_])
# print(timer() - time)
# best_model.evaluate(x_batch[0:20], y_batch[0:20])
# print('ok?')

# [-69.99014799098367, {'activation': <function relu at 0x00000215C0B86620>, 'batch_size': 128, 'epochs': 700, 'layers': [50, 70]}]
# [-68.68425594968505, {'activation': <function relu at 0x00000293163BC620>, 'batch_size': 128, 'epochs': 700, 'layers': [45, 60, 90]}]
# [-68.34868468302862, {'activation': <function relu at 0x000001F1E425C620>, 'batch_size': 128, 'epochs': 700, 'layers': [70, 120]}]
# [-64.25238957167741, {'activation': <function relu at 0x0000020C055B7620>, 'batch_size': 128, 'epochs': 700, 'layers': [50, 100, 150, 100, 80, 60, 30]}]

# 700 epochs


# for x in range(1):
#     learning_rate=0.01
#     model = Sequential()
#     model.add(Dense(10, input_dim=4, activation='relu'))  # 1st hidden layer; states as input
#     model.add(Dense(50, activation='relu'))
#     model.add(Dense(4, activation='linear'))
#     model.compile(loss='mse',
#                   optimizer=Adam(lr=learning_rate))
#     x=model.fit(x_batch, y_batch,batch_size=len(x_batch), epochs=90,validation_split=0.2,verbose=0)
# print(x.history['loss'][-1])
# pred = model.predict(np.array([[1,7,1,2]]))
# print(pred)
# model.evaluate(x_batch,y_batch)
# pass
# for i in range(10):
#     model.fit(x_batch, y_batch,batch_size=len(x_batch), epochs=40,validation_split=0.2,verbose=0)
# pred=model.predict(x_batch)
# print(pred)

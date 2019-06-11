import numpy as np
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.activations import sigmoid, relu
from tensorflow.python.keras.layers import Dense, Activation
from tensorflow.python.keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import GridSearchCV
from timeit import default_timer as timer

def create_model(layers, activation):
    global a
    print('x',a)
    a+=1
    model = Sequential()
    for i, nodes in enumerate(layers):
        if i == 0:
            model.add(Dense(nodes, input_dim=4))
            model.add(Activation(activation))
        else:
            model.add(Dense(nodes))
            model.add(Activation(activation))
    model.add(Dense(4))  # Note: no activation beyond this point

    model.compile(optimizer='adadelta', loss='mse')
    return model

time=timer()
x_batch=np.array(np.loadtxt('x_batch.txt',delimiter=','))
y_batch=np.array(np.loadtxt('y_batch.txt',delimiter=','))

model = KerasRegressor(build_fn=create_model, verbose=0)
layers = [[30], [40, 20], [45, 30, 15],[30,10],[50,70],[20,30],[40,70]]
activations = [sigmoid, relu]
param_grid = dict(layers=layers, activation=activations, batch_size = [128, 256], epochs=[700])
a=1
grid = GridSearchCV(estimator=model, param_grid=param_grid, scoring='neg_mean_squared_error')
# print(len(x_batch))
grid_result = grid.fit(x_batch[0:2000], y_batch[0:2000])

print([grid_result.best_score_, grid_result.best_params_])
print(timer()-time)












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
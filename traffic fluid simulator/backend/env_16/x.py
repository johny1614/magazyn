# import tensorflow as tf
import numpy as np
import tensorflow.keras as keras
from tensorflow.python.keras.optimizers import Adam
import random

# # Dla 1 wymiaru ok
# model = keras.models.Sequential()
# model.add(keras.layers.Dense(3, activation='relu', input_dim=1))
# model.add(keras.layers.Dense(5, activation='relu'))
# model.add(keras.layers.Dense(1))
# model.compile(loss='mse',optimizer=Adam())
#
# x=np.array([i for i in range(10)])
# y=np.array([i+2 for i in range(10)])
#
# model.fit(x,y,epochs=1000)
# predictions = model.predict(x)
# diffs=[(predictions[i]-y[i])**2 for i in range(len(predictions))]
# mse=sum(diffs)/len(diffs)
# a=34



model = keras.models.Sequential()
model.add(keras.layers.Dense(7, activation='relu', input_dim=1))
model.add(keras.layers.Dense(12, activation='relu'))
model.add(keras.layers.Dense(10, activation='relu'))
model.add(keras.layers.Dense(2))
model.compile(loss='mse',optimizer=Adam())

x=np.array([i for i in range(10)])
y=np.array([[i+2,i**2+6] for i in range(10)])
inne=0
te_same=0
for a in range(100000):
    weights_before = model.get_weights()
    model.fit(x,y,epochs=10,verbose=0)
    same=True
    porownanie = weights_before[0] == model.get_weights()[0]
    for porownanie_warstwa in porownanie:
        if any([s == False for s in porownanie_warstwa]):
            same = False
    if same:
        te_same+=1
        print(f'wagi te same {te_same} inne {inne}')
    else:
        inne+=1
    # predictions = model.predict(x)
    # diffs=[(predictions[i]-y[i])**2 for i in range(len(predictions))]
    # mse=sum(sum(diffs))/len(predictions)/len(predictions[0])
    # print('mse',mse)
# a=34

# a=[0,1,2,3,4]
# b=[2,4,8,10,12]
# print(random.sample([(x,y) for x in ran],2))
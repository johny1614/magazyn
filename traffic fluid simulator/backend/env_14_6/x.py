# import tensorflow as tf
import numpy as np
import tensorflow.keras as keras
from tensorflow.python.keras.optimizers import Adam


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
y=np.array([[i+2-i**5,i**2+6] for i in range(10)])

model.fit(x,y,epochs=1000,validation_split=0.2)
predictions = model.predict(x)
diffs=[(predictions[i]-y[i])**2 for i in range(len(predictions))]
mse=sum(sum(diffs))/len(predictions)/len(predictions[0])
print('mse',mse)
a=34
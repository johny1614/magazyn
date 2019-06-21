from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.optimizers import Adam
from tensorflow.python.keras import regularizers
import matplotlib.pyplot as plt
import numpy as np
model = Sequential()
model.add(Dense(8, activation='relu', kernel_regularizer=regularizers.l2(0.001), input_shape = (1,)))
model.add(Dense(8, activation='relu', kernel_regularizer=regularizers.l2(0.001)))
model.add(Dense(1))

model.compile(optimizer=Adam(),loss='mse')

# generate 10,000 random numbers in [-50, 50], along with their squares
x = np.random.random((10000,1))*100-50
y = x**2

# fit the model, keeping 2,000 samples as validation set
hist = model.fit(x,y,validation_split=0.2,
             epochs= 15000,
             batch_size=256)

# check some predictions:
print(model.predict([4, -4, 11, 20, 8, -5]))
# result:
# [[ 16.633354]
#  [ 15.031291]
#  [121.26833 ]
#  [397.78638 ]
#  [ 65.70035 ]
#  [ 27.040245]]
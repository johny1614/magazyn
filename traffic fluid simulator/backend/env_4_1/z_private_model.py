import numpy as np
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.optimizers import Adam

x_batch=np.array(np.loadtxt('x_batch.txt',delimiter=','))
y_batch=np.array(np.loadtxt('y_batch.txt',delimiter=','))

learning_rate=0.01
model = Sequential()
model.add(Dense(10, input_dim=3, activation='relu'))  # 1st hidden layer; states as input
model.add(Dense(20, activation='relu'))
model.add(Dense(4, activation='linear'))
model.compile(loss='mse',
              optimizer=Adam(lr=learning_rate))
for i in range(10):
    model.fit(x_batch, y_batch,batch_size=len(x_batch), epochs=40,validation_split=0.2,verbose=0)
    pred = model.predict(np.array([[6,1,1]]))
    print(pred)
pred=model.predict(x_batch)
# print(pred)
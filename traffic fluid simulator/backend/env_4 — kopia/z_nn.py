import numpy as np
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.optimizers import Adam


x=np.array(np.random.random((1000,1))*100-30)
# x = np.array([x for x in range(30)])
y = np.array([i*i - 20*i +4 for i in x])

model = Sequential()
model.add(Dense(10,input_dim=1,activation='relu'))
model.add(Dense(20,activation='relu'))
model.add(Dense(1))
learning_rate=0.01
model.compile(loss='mse',optimizer=Adam(learning_rate))

model.fit(x=x,y=y,epochs=1050,verbose=0)
#
# predictions=model.predict(x)
model.evaluate(x=x,y=y)
# print(x)
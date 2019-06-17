import random

import numpy as np
from tensorflow.python.keras.losses import huber_loss
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.python.keras.layers import BatchNormalization


def get_memory():
    memory = [
        #  x - 3 gestosci + aktualna faza
        # {'state': [55, 1, 1, 1], 'new_state': [0, 1, 1, 1], 'action': 1, 'reward': 40},
        # {'state': [96, 1, 1, 1], 'new_state': [0, 1, 1, 1], 'action': 1, 'reward': 70},
        # {'state': [70, 1, 1, 1], 'new_state': [0, 1, 1, 1], 'action': 1, 'reward': 60},
        # {'state': [0, 25, 0, 0], 'new_state': [0, 0, 1, 1], 'action': 2, 'reward': 60},
        # {'state': [0, 25, 0, 0], 'new_state': [0, 0, 1, 1], 'action': 2, 'reward': -60},
        {'state': [0, 25, 0, 0], 'new_state': [0, 0, 1, 1], 'action': 2, 'reward': 60},
        {'state': [0, 25, 0, 0], 'new_state': [0, 0, 1, 1], 'action': 2, 'reward': 60},
        {'state': [0, 25, 0, 0], 'new_state': [0, 0, 1, 1], 'action': 2, 'reward': 60},
        {'state': [0, 25, 0, 0], 'new_state': [0, 0, 1, 1], 'action': 2, 'reward': 60},
        {'state': [0, 25, 0, 0], 'new_state': [0, 0, 1, 1], 'action': 2, 'reward': 60},
        {'state': [0, 25, 0, 0], 'new_state': [0, 0, 1, 1], 'action': 2, 'reward': 60},
        {'state': [0, 25, 0, 0], 'new_state': [0, 0, 1, 1], 'action': 2, 'reward': 60},
        {'state': [0, 25, 0, 0], 'new_state': [0, 0, 1, 1], 'action': 2, 'reward': 60},
        {'state': [0, 25, 0, 0], 'new_state': [0, 0, 1, 1], 'action': 2, 'reward': 60},
        {'state': [0, 25, 0, 0], 'new_state': [0, 0, 1, 1], 'action': 2, 'reward': 60},
        {'state': [0, 25, 0, 0], 'new_state': [0, 0, 1, 1], 'action': 2, 'reward': 60},
        {'state': [0, 25, 0, 0], 'new_state': [0, 0, 1, 1], 'action': 2, 'reward': 60},
    ]
    return memory

def get_memory2():
    return [
        {'state': [0, 25, 0, 0], 'new_state': [0, 0, 1, 1], 'action': 2, 'reward': -300},
        # {'state': [0, 25, 0, 0], 'new_state': [0, 0, 1, 1], 'action': 2, 'reward': 30},
        # {'state': [0, 25, 0, 0], 'new_state': [0, 0, 1, 1], 'action': 2, 'reward': 30},
        # {'state': [0, 25, 0, 0], 'new_state': [0, 0, 1, 1], 'action': 2, 'reward': 30},
        # {'state': [0, 25, 0, 0], 'new_state': [0, 0, 1, 1], 'action': 2, 'reward': 30},

    ]

def get_more_memory():
    # memory=get_memory()
    # memory.append(
    #     {'state': [0, 25, 0, 0], 'new_state': [0, 0, 1, 1], 'action': 2, 'reward': 0},
    # )
    # return memory
    return [{'state': [0, 25, 0, 0], 'new_state': [0, 0, 1, 1], 'action': 2, 'reward': 0}]


def _build_model():
    # neural net to approximate Q-value function:
    model = Sequential()
    # model.add(Dense(Globals().l1, input_dim=3, activation='relu'))  # 1st hidden layer; states as input
    # model.add(Dense(Globals().l2, activation='relu'))  # 2nd hidden layer
    # model.add(Dense(Globals().l3, activation='relu'))  # 2nd hidden layer
    # model.add(Dense(4, activation='linear'))  # 2 actions, so 2 output neurons: 0 and 1 (L/R)

    model.add(Dense(12, input_dim=4, activation='linear'))  # 1st hidden layer; states as input
    # model.add(BatchNormalization())
    model.add(Dense(40, activation='relu'))
    model.add(Dense(4, activation='linear'))
    model.compile(loss=huber_loss,
                  optimizer=Adam())
    return model

def get_batches(memoriez):
    gamma = 0
    x_batch = []
    y_batch = []
    batch_size=5
    minibatch = random.sample(memoriez, min(len(memoriez), batch_size))
    for memory in minibatch:
        state = memory['state']
        new_state = memory['new_state']
        y_target = model.predict(np.array([state]))[0]
        target = (memory['reward'] + gamma *  # (target) = reward + (discount rate gamma) *
                  np.amax(model.predict(np.array([new_state]))))  # (maximum target Q based on future action a')
        y_target[memory['action']] = target
        x_batch.append(state)
        y_batch.append(y_target)
    return x_batch,y_batch


def replay():
    while True:
        x_batch,y_batch=get_batches(memories)
        x_batch_2,y_batch_2=get_batches(memories2)

        # print(x_batch)
        res = model.fit(np.array(x_batch), np.array(y_batch), epochs=60, batch_size=len(x_batch), verbose=0)
            # print(model.predict(np.array([[0, 25, 0, 0]])))
        print(res.history['loss'][-1])
        # print(res.history['val_loss'][-1])
        # model.evaluate(np.array(x_batch),np.array(y_batch))
        # print(res.history['val_loss'][-1])
        i = 4
    # res2=model.evaluate(np.array(x_batch), np.array(y_batch))
    # print(res2)
    # more_memory=get_more_memory()
    # for memory in more_memory:
    #     state = memory['state']
    #     new_state = memory['new_state']
    #     y_target = model.predict(np.array([state]))[0]
    #     target = (memory['reward'] + gamma *  # (target) = reward + (discount rate gamma) *
    #               np.amax(model.predict(np.array([new_state]))))  # (maximum target Q based on future action a')
    #     y_target[memory['action']] = target
    #     x_batch.append(state)
    #     y_batch.append(y_target)
    # res=model.fit(np.array(x_batch), np.array(y_batch), epochs=7000, batch_size=len(x_batch), verbose=0)
    # res2=model.evaluate(np.array(x_batch), np.array(y_batch))
    # print(res2)


memories = get_memory()
memories2 = get_memory2()
model = _build_model()
replay()

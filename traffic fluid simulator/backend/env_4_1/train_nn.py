import os

from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.optimizers import Adam
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from nn_data import S1, S2


def dA(s1, s2):
    result = 0
    result += abs(s1[0] - s2[0])
    result += abs(s1[1] - s2[1])
    result += abs(s1[2] - s2[2])
    for i in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]:
        result += 0.4 * abs(s1[i] - s2[i])
    result += 2 * abs(s1[15] - s2[15])
    result += abs(s1[16] - s2[16])
    return result

def dB(s1, s2):
    result = 0
    for i in [0, 1, 2, 3]:
        result += abs(s1[i] - s2[i])
    return result


model = Sequential([
    Dense(16, input_shape=(1,), activation='relu'),
    Dense(32, activation='relu'),
    Dense(2, activation='softmax')]
)
model.compile(Adam(lr=0.0001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
# model.fit(scaled_train_samples, train_labels, batch_size=20, epochs=10, validation_split=0.2, shuffle=True, verbose=2)

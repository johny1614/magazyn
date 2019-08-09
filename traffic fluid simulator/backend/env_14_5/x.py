# import tensorflow as tf
import tensorflow.keras as keras
model = keras.models.Sequential()
model.add(keras.layers.Dense(3, activation='relu', input_dim=3))
model.add(keras.layers.Dense(5, activation='relu'))
model.add(keras.layers.Dense(2, activation='softmax'))
keras.utils.plot_model(model, to_file='model.png', show_shapes=True)
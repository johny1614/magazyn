from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time
from datetime import datetime
from packaging import version
import tensorflow as tf
from tensorflow import keras

import numpy as np

print("TensorFlow version: ", tf.__version__)
assert version.parse(tf.__version__).release[0] >= 2, \
    "This notebook requires TensorFlow 2.0 or above."
data_size = 1000
# 80% of the data is for training.
train_pct = 0.1

train_size = int(data_size * train_pct)

# Create some input data between -1 and 1 and randomize it.
x = np.linspace(-1, 1, data_size)
np.random.shuffle(x)

# Generate the output data.
# y = 0.5x + 2 + noise
y = 0.5 * x + 2 + np.random.normal(0, 0.05, (data_size,))

# Split into test and train pairs.
x_train, y_train = x[:train_size], y[:train_size]
x_test, y_test = x[train_size:], y[train_size:]
# logdir="logs_l_rate" + datetime.now().strftime("%Y%m%d-%H%M%S")
logdir = "logs_l_ratee"
# tensorboard_callback = keras.callbacks.TensorBoard(log_dir=logdir)
#
# model = keras.models.Sequential([
#     keras.layers.Dense(16, input_dim=1),
#     keras.layers.Dense(1),
# ])
#
# model.compile(
#     loss='mse', # keras.losses.mean_squared_error
#     optimizer=keras.optimizers.SGD(lr=0.2),
# )
#
# print("Training ... With default parameters, this takes less than 10 seconds.")
# training_history = model.fit(
#     x_train, # input
#     y_train, # output
#     batch_size=train_size,
#     verbose=0, # Suppress chatty output; use Tensorboard instead
#     epochs=100,
#     validation_data=(x_test, y_test),
#     callbacks=[tensorboard_callback],
# )
#
# print("Average test loss: ", np.average(training_history.history['loss']))
# print(model.predict([60, 25, 2]))
# # True values to compare predictions against:
# # [[32.0]
# #  [14.5]
# #  [ 3.0]]

# logdir = "logs/scalars/" + datetime.now().strftime("%Y%m%d-%H%M%S")
file_writer = tf.summary.create_file_writer(logdir + "/metrics")
file_writer.set_as_default()


def lr_schedule(epoch):
    """
    Returns a custom learning rate that decreases as epochs progress.
    """
    learning_rate = 0.1
    # learning_rate = 0.2
    # if epoch > 10:
    #     learning_rate = 0.02
    # if epoch > 20:
    #     learning_rate = 0.01
    # if epoch > 50:
    #     learning_rate = 0.005
    # tf.summary.scalar('learning rate', data=learning_rate, step=epoch)
    return learning_rate


# def cokolwiek(a=10, b=20, c=33):
#     if a > 2:
#         return 10.0
#     else:
#         return 50.0

def log_weights(epoch,logs):
    print(f'epoch:{epoch} wagi: {model.layers[0].get_weights()}')
    weight0 = model.get_weights()[0][0][0]
    weight1 = model.get_weights()[0][0][1]
    # tf.summary.scalar('weights0', data=weight0, step=epoch)
    # tf.summary.scalar('weights1', data=weight1, step=epoch)
    # tf.summary.histogram(name='weights_hist',data = weight0,step=epoch)
    # print(batch)

csv_logger = keras.callbacks.CSVLogger('training.log')
# cokolwik_callback = keras.callbacks.LearningRateScheduler(cokolwiek)
lr_callback = keras.callbacks.LearningRateScheduler(lr_schedule)
tensorboard_callback = keras.callbacks.TensorBoard(log_dir=logdir,histogram_freq=1)

print_weights = keras.callbacks.LambdaCallback(on_epoch_end=log_weights)


model = keras.models.Sequential([
    keras.layers.Dense(16, input_dim=1),
    keras.layers.Dense(1),
])

model.compile(
    loss='mse',  # keras.losses.mean_squared_error
    optimizer=keras.optimizers.SGD(),
)

training_history = model.fit(
    x_train,  # input
    y_train,  # output
    batch_size=train_size,
    verbose=0,  # Suppress chatty output; use Tensorboard instead
    epochs=100,
    validation_data=(x_test, y_test),
    callbacks=[tensorboard_callback, lr_callback, csv_logger, print_weights],
    shuffle=True
)
a = 6

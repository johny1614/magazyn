import tensorflow as tf
import numpy as np
import edward as ed
from tensorflow.python.ops.distributions.normal import Normal


def build_toy_dataset(N, w):
  D = len(w)
  x = np.random.normal(0.0, 2.0, size=(N, D))
  y = np.dot(x, w) + np.random.normal(0.0, 0.01, size=N)
  return x, y

ed.set_seed(42)

N = 40  # number of data points
D = 5  # number of features

w_true = np.random.randn(D) * 0.5
X_train, y_train = build_toy_dataset(N, w_true)
X_test, y_test = build_toy_dataset(N, w_true)
#
# with tf.name_scope("model"):
#   X = tf.placeholder(tf.float32, [N, D], name="X")
#   w = Normal(loc=tf.zeros(D, name="weights/loc"),
#              scale=tf.ones(D, name="weights/scale"),
#              name="weights")
#   b = Normal(loc=tf.zeros(1, name="bias/loc"),
#              scale=tf.ones(1, name="bias/scale"),
#              name="bias")
#   y = Normal(loc=ed.dot(X, w) + b,
#              scale=tf.ones(N, name="y/scale"),
#              name="y")
import random
from typing import List
import attr
import numpy as np
from tensorflow.python.keras.callbacks import TensorBoard, LambdaCallback

import env_settings


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ValParamSet:
    def __init__(self, layers, nn_l_rate, first_epochs_range, epochs_range, max_time_learn, gamma, batch_size,
                 reshape_future):
        # self.layers = layers
        # self.nn_l_rate = nn_l_rate
        # self.first_epochs_range = first_epochs_range
        # self.epochs_range = epochs_range
        # self.max_time_learn = max_time_learn
        # self.layers = [18,22,30,20,16,10]
        self.layers = [10, 12, 10]  # u =2,98 maksymalnie
        self.nn_l_rate = 0.01
        self.q_formula_l_rate = 0.2
        self.first_epochs_range = 2
        self.epochs_range = 20
        self.batch_size = 64
        self.max_time_greedy = 1000
        self.max_time_learn = 300
        self.gamma = 0.9
        self.reshape_future = 0
        self.regularization = 0.1
        self.epochs_learn = 5

    def __str__(self):
        return f'layers = {self.layers} nn_l_rate = {self.nn_l_rate} first_epochs_range = {self.first_epochs_range} epochs_range = {self.epochs_range} max_time_learn = {self.max_time_learn}'


def create_vals():
    layerss = [[10], [10, 10], [6, 10], [10, 6]]
    nn_l_rates = [0.1 ** 4, 0.1 ** 3, 0.1 ** 2, 0.05]
    first_epochs_ranges = [10, 20, 30]
    epochs_ranges = [20, 40, 50, 80, 100]
    max_time_learns = [15, 30, 40, 70]
    vParams = []
    reshape_future = 3
    gamma = 0.9
    batch_size = 1000
    for layers in layerss:
        for nn_l_rate in nn_l_rates:
            for first_epochs_range in first_epochs_ranges:
                for epochs_range in epochs_ranges:
                    for max_time_learn in max_time_learns:
                        v = ValParamSet(layers, nn_l_rate, first_epochs_range, epochs_range, max_time_learn, gamma,
                                        batch_size, reshape_future)
                        vParams.append(v)
    random.shuffle(vParams)
    return vParams


class BaseClass:
    def __init__(self):
        self.val_params: List[ValParamSet] = create_vals()
        self.time = 0
        self.epochs_learn_done = 0
        self.state_repeats = 0
        # self.max_time_random = 1000
        self.new_states = 0
        # self.epochs_learn = 2
        self.batch_size = 60
        self.validation_batch_size = 20
        self.actions_memory = [0, 0, 0, 0]
        self.l1 = 8
        self.l2 = 168
        self.l3 = 54
        self.x_batch = []
        self.y_batch = []
        self.max_epsilon = 1
        self.min_epsilon = 0.01
        self.epsilon = 0.2
        self.pred_plot_memory = []
        self.run_no = 0
        self.greedy_run_no = 0
        self.actual_epoch_index = 0
        self.last_weights = None
        self.not_to_learn_last_epochs = 10
        self.global_rewards_mem = []
        name = "nn_l_rate={} layers={}".format(self.vp().nn_l_rate, self.vp().layers)
        self.tensorboard = TensorBoard(log_dir="logs\{}".format(name))
        print('TEEEEEEEEEEEEEEEEnsorboard')
        self.epochs_learn_done = 0
        self.y_batch_check = None
        self.x_batch_check = None
        self.x_batch_history = []
        self.y_batch_history = []
        self.nn_x_batch_history = []
        self.nn_y_batch_history = []
        self.u_value = 1
        # self.u_value = 5.159780351999999
        self.cars_out_memory = []
        self.cars_in_memory = []

    def vp(self) -> ValParamSet:
        return self.val_params[self.run_no]

    def get_u(self, time):
        u = Globals().u_value
        return np.array([[u] * time] * len(env_settings.source_sections)).transpose()

    def get_u_train(self, epoch):
        # if 0<= epoch <3:
        #     return env_settings.generate_u(1)
        # if 3<= epoch <6:
        #     return env_settings.generate_u(2)
        # if 6<= epoch <9:
        #     return env_settings.generate_u(2)
        # if 9<= epoch <12:
        #     return env_settings.generate_u(3)
        # else:
        #     return env_settings.generate_u(4)
        return env_settings.generate_u(self.u_value)

    # def epsilon(self):
    #     epsilon_decay = 0.96
    #     epsilon = self.min_epsilon + epsilon_decay ** self.epochs_done
    #     epsilon = epsilon if epsilon > self.min_epsilon else self.min_epsilon
    #     epsilon = epsilon if epsilon < self.max_epsilon else self.max_epsilon
    #     return epsilon


class Globals(BaseClass, metaclass=Singleton):
    pass

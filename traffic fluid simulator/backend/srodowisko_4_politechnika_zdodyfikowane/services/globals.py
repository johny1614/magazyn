import numpy as np
import env_settings


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ValParamSet:
    def __init__(self):
        self.layers = [14, 18, 10]
        self.nn_l_rate = 0.01
        self.q_formula_l_rate = 0.2
        self.first_epochs_range = 2
        self.epochs_range = 20
        self.batch_size = 64
        self.max_time_greedy = 1000
        self.max_time_learn = 300
        self.gamma = 0.9
        self.reshape_future = 0
        self.epochs_learn = 5


class BaseClass:
    def __init__(self):
        self.vp = ValParamSet()
        self.time = 0
        self.epochs_learn_done = 0
        self.actions_memory = [0, 0, 0, 0]
        self.epsilon = 0.2
        self.greedy_run_no = 0
        self.actual_epoch_index = 0
        self.not_to_learn_last_epochs = 10
        self.epochs_learn_done = 0
        self.u_value = 1
        self.cars_out_memory = []

    def get_u(self, time):
        EX = self.u_value # u_value to EX
        sigma_par = 0.4
        mean_par = np.log(EX) - sigma_par * sigma_par / 2
        u=2
        mine= np.array([[np.random.lognormal(mean=mean_par, sigma=sigma_par) for x in range(time)] for x in env_settings.source_sections]).transpose()
        old=np.array([[u] * time] * len(env_settings.source_sections)).transpose()
        return mine


class Globals(BaseClass, metaclass=Singleton):
    pass

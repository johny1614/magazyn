import env_settings


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ValParamSet:
    def __init__(self):
        self.layers = [10, 14, 10]
        self.nn_l_rate = 0.01
        self.epochs_range = 10
        self.batch_size = 1000
        self.max_time_learn = 70
        self.gamma = 0.9
        self.reshape_future = 0
        self.regularization = 0.1

    def __str__(self):
        return f'layers = {self.layers} nn_l_rate = {self.nn_l_rate} first_epochs_range = {self.first_epochs_range} epochs_range = {self.epochs_range} max_time_learn = {self.max_time_learn}'


class BaseClass:
    def __init__(self):
        self.time = 0
        self.epochs_done = 0
        self.epochs_learn = 10
        self.learning_rate = 1 # we wzorze na q
        self.batch_size = 60
        self.epsilon = 1
        self.pred_plot_memory = []
        self.greedy_run_no = 0
        self.actual_epoch_index = 0
        self.not_to_learn_last_intervals = 10
        self.epochs_done = 0
        self.u = env_settings.u_all_2
        self.vp=ValParamSet()


class Globals(BaseClass, metaclass=Singleton):
    pass

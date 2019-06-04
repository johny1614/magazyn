class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class BaseClass:
    def __init__(self):
        self.time = 0
        self.epochs_done = 0
        self.state_repeats = 0
        self.new_states = 0
        self.epochs_learn = 10
        self.gamma = 0.8
        self.learning_rate = 0.001
        self.batch_size = 50

    def epsilon(self):
        min_epsilon = 0.01
        epsilon_decay = 0.995
        return min_epsilon + epsilon_decay ** self.epochs_done


class Globals(BaseClass, metaclass=Singleton):
    pass

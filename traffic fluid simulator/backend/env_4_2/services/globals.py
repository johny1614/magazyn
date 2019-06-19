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
        self.gamma = 0
        self.learning_rate = 0.005
        self.batch_size = 60
        self.validation_batch_size=20
        self.l1=8
        self.l2=168
        self.l3=54
        self.x_batch=[]
        self.y_batch=[]
        self.max_epsilon=1
        self.min_epsilon = 0.01
        self.goodmemes = []

    def epsilon(self):
        epsilon_decay = 0.99
        epsilon = self.min_epsilon + epsilon_decay ** self.epochs_done
        epsilon = epsilon if epsilon > self.min_epsilon else self.min_epsilon
        epsilon = epsilon if epsilon < self.max_epsilon else self.max_epsilon
        return epsilon


class Globals(BaseClass, metaclass=Singleton):
    pass

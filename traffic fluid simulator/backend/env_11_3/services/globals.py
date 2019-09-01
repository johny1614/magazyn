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
        self.gamma = 0
        self.learning_rate = 1
        self.batch_size = 60
        self.x_batch=[]
        self.y_batch=[]
        self.epsilon=1
        self.pred_plot_memory=[]
        self.learn_iteration=0
        self.greedy_run_no=0

class Globals(BaseClass, metaclass=Singleton):
    pass

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class BaseClass:
    def __init__(self):
        self.time = 0
        self.state_repeats = 0
        self.new_states=0
        self.time_a=0
        self.time_b=0
        self.time_c=0
        self.time_d=0
    def epsilon(self):
        return 0.01


class Globals(BaseClass, metaclass=Singleton):
    pass

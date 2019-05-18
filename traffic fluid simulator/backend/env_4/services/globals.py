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


class Globals(BaseClass, metaclass=Singleton):
    pass

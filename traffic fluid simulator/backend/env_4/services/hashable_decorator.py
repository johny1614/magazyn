def hashable(*args):
    def wrapper(cls):
        setattr(cls, '__hash__', eval('__hash__'))
        setattr(cls, '__eq__', eval('__eq__'))
        return cls
    return wrapper


def __hash__(self):
    all_properties = [prop for prop in self.hash_keys if not prop.startswith('__')]
    values = tuple([getattr(self, prop) for prop in all_properties])
    return hash(values)


def __eq__(self, other):
    return self.__hash__() == other.__hash__()

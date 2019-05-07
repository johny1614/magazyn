import string
from dataclasses import dataclass


def hashable(name):
    print(name)
    def wrapper(cls):
        setattr(cls, '__hash__', eval('__hash__'))
        return cls
    return wrapper

def __hash__(self):
    all_properties = [prop for prop in dir(self) if not prop.startswith('__')]
    values = tuple([getattr(self, prop) for prop in all_properties])
    return hash(values)



@hashable('name')
@dataclass
class Dog:
    name: string
    height: int

azor: Dog = Dog('azor',50)
fafik: Dog = Dog('fafik',20)
fafik2: Dog = Dog('fafik',24)
print(azor.__hash__())
print(fafik.__hash__())
print(fafik2.__hash__())
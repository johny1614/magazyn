import string
from dataclasses import dataclass
from typing import List

from services.hashable_decorator import hashable


@dataclass
@hashable()
class Dog:
    name: string
    age: int
    hash_keys = ['name']

dog = Dog(name='azor', age=23)
dog2= Dog(name='fafik',age=22)
dog3 = Dog(name='azor', age=233)
print(dog.__hash__())
print(dog2.__hash__())
print(dog3.__hash__())

dic={dog:[2],dog2:'tez dobry',dog3:[5]}
dic[dog3].append(34)
dic[dog].append(235)
print(dic)
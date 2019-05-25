class Dog:
    def __init__(self):
        self.name = 'azor'
        self.age = 34

    def __hash__(self):
        return hash((self.age, self.name))


dog1 = Dog()
dog2 = Dog()
pass

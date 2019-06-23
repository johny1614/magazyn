class Dog:
    def __init__(self):
        self.name='johny'
        self.age=22
        self.sex='yes'
def get_G(rewards, gamma):
    G = [0] * len(rewards)
    G_value = rewards[-1]
    G[len(rewards) - 1] = G_value
    for i in reversed(range(len(rewards) - 1)):
        G_value = gamma * G_value + rewards[i]
        G[i]=G_value
    return G
def to_array(ob):
    arr = []
    for attr, value in ob.__dict__.items():
        arr.append(value)
    return arr

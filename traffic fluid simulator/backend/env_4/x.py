class Dog:
    def __init__(self, id, no):
        self.id = id
        self.no = no

    def __str__(self):
        return 'Dog:  id=' + self.id

    def __eq__(self, other):
        # print('eq')
        return self.id == other.id and self.no == other.no

    def __hash__(self):
        return hash(tuple([self.id,self.no]))


names = {}
dog1 = Dog(1, 3)
dog2 = Dog(2, 3)
dog1_again = Dog(1, 56)

names[(1, dog1)] = "siema"
names[(1, dog2)] = "ehehe"
names[(1, dog1_again)] = "elooooooooo!"
names[(1, dog1_again)] = "eloooooooooxd!"
# print(dog1)
#
print(names)
a = ('2',)
b = 'z'
a = a + (b,)
print(a)
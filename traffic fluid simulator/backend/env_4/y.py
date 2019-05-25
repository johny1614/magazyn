import copy
a=[1, 2, [3,5], 4]
b=copy.copy(a)
b[2][0] = 7
b[0]=234
print(a)
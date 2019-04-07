# from env import  Env
import numpy as np
# np1=tuple([2,3,4])
# np2=tuple([2,3,6])
# V={np1:1,np2:2}
# new_V={key:0 for key in V}
# for key in new_V:
#     print(key)
#     print(new_V[key])
# state_space=[ (x,y,z) for x in range(40) for y in range(40) for z in range(40)]
# print(state_space.__len__())
dic={}
# A_a_green = np.array([1,2,3,4])
# dic[(1,2)]=12
# dic[tuple(A_a_green)]=14
# print(tuple(A_a_green))
# kolejne= np.array([1,2,3,4])
# print(dic[hash(tuple(kolejne))])
c=np.array([[0, 0, 0],  # A
                      [0, 1, 0], # B
                      [1, 0, 0]])# C
hashable_c=[tuple(x) for x in c]
print(hashable_c)
# print(tuple(tuple(c)))
# print(hash(tuple(tuple(c))))
# dic[tuple(tuple(c))]=141
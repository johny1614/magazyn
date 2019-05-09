# import string
#
# from model.LearningState import LearningState
#
# state_1 = LearningState(pre_cross_densities=(0, 4, 5), global_aggregated_densities=(2, 4, 5), phase_no=2,
#                         phase_duration=1)
# different_state = LearningState(pre_cross_densities=(0, 4, 5), global_aggregated_densities=(2, 4, 8), phase_no=2,
#                                 phase_duration=1)
# state_1_also = LearningState(pre_cross_densities=(0, 4, 5), global_aggregated_densities=(2, 4, 5), phase_no=2,
#                              phase_duration=1)
# myDic = {state_1: [2], different_state: [7]}
# myDic[state_1_also].append(6)
# print(myDic[state_1])
# # import string
# #
# import attr
#
#
# @attr.s(auto_attribs=True)
# class Animal:
#     ssie: bool
#     foots: int = 5
#     smart: string = 'yes'
#
#
# @attr.s(auto_attribs=True)
# class Dog(Animal):
#     name: string = 'BezImenny'
#     # def __init__(self,name):
#     # self.name=name
#
#
# # @attr.s
# # class Coordinates(object):
# #     x = attr.ib()
# #     y = attr.ib()
# #
# #
# # cord = Coordinates(x=12, y=5)
# # cord_2 = Coordinates(x=17, y=5)
# # cord_also = Coordinates(x=12, y=5)
# dog = Dog(name='Azor', foots=4,ssie=True)
# dog_also = Dog(name='Azor', foots=4,ssie=True)
# # print('cord==cord_also', cord == cord_also)
# print('dog==dog_also', dog == dog_also)
import numpy as np

a = np.zeros([36, 36])
print(a)

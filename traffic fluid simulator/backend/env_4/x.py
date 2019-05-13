# from dataclasses import dataclass, field
# from typing import List
#
# import attr
#
#
# def empty_list():
#     return []
#
#
# @attr.s(auto_attribs=True)
# class Env:
#     lista: List = attr.Factory(list)
#
#
# env = Env()
# env.lista.append(23)
# # del env
# env = Env()
# print(env)

import matplotlib.pyplot as plt
scores=[2,45,23,432,52,33,44]
plt.plot(scores)
plt.show()
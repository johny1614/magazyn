import numpy as np
from services.globals import Globals

not_last_sections = [i for i in range(36) if i not in [29, 32, 35]]

stayCoordinates = [(2, 2),
                   (5, 5),
                   (8, 8),
                   (11, 11),
                   (14, 14),
                   (17, 17),
                   (20, 20),
                   (23, 23),
                   (26, 26),
                   ]
freeMovementCoordinates = [(1, 0), (2, 1), (2, 2),
                           (4, 3), (5, 4), (5, 5),
                           (7, 6), (8, 7), (8, 8),
                           (10, 9), (11, 10), (11, 11),
                           (13, 12), (14, 13), (14, 14),
                           (16, 15), (17, 16), (17, 17),
                           (19, 18), (20, 19), (20, 20),
                           (22, 21), (23, 22), (23, 23),
                           (25, 24), (26, 25), (26, 26),
                           (28, 27), (29, 28),
                           (31, 30), (32, 31),
                           (34, 33), (35, 34)]
sections_of_roads = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [9, 10, 11],
    [12, 13, 14],
    [15, 16, 17],
    [18, 19, 20],
    [21, 22, 23],
    [24, 25, 26],
    [27, 28, 29],
    [30, 31, 32],
    [33, 34, 35],
]
source_sections = [0, 3, 6]


x_size = 36


def start_A():
    # it is a red light everywhere A matrix
    A = np.zeros((x_size, x_size))
    for cord in freeMovementCoordinates + stayCoordinates:
        A[cord] = 1
    return A


def get_x():
    x = [x_size * [0]]
    return x


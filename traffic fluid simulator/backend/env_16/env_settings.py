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


def generate_u(cars_incoming):
    return np.array([[cars_incoming] * max_time] * 3).transpose()


def get_u_under_15_random():
    random_numbers_road_0 = []
    random_numbers_road_1 = []
    for i in range(90):
        random_numbers_road_0.append(np.random.random() * 15)
        random_numbers_road_1.append(np.random.random() * 15)
    return np.array([random_numbers_road_0, random_numbers_road_1]).transpose()


def get_u_under_x_random(x):
    random_numbers_road_0 = []
    random_numbers_road_1 = []
    for i in range(90):
        random_numbers_road_0.append(np.random.random() * x)
        random_numbers_road_1.append(np.random.random() * x)
    return np.array([random_numbers_road_0, random_numbers_road_1]).transpose()


#
# env_settings_A_storage = [[]] * max_time
#
# u_v1 = np.array([[4, 4, 4, 60, 4, 4, 4, 4, 4, 4, 4, 60, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 60, 4, 4, 4, 4, 4, 4, 4,
#                   4, 4, 4, 60, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 60, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 60, 4, 4,
#                   4, 4, 4, 4, 60, 4, 4,
#                   4, 4, 4, 4, 60, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 60, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
#                   60, 4, 4, 4, 4, 4, 4,
#                   4, 4, 4, 4, 4, 4, 4]]).transpose()
#
# u_all_2 = np.array([[2] * max_time, [2] * max_time]).transpose()
# #
# u_all_4 = np.array([[4] * max_time,[4] * max_time]).transpose()
# #
# #
# u_all_9 = np.array([[9] * max_time, [9] * max_time]).transpose()
#
# u_under_15_random = get_u_under_15_random()
#
u = np.array([[1] * Globals().vp().max_time_learn, [1] * Globals().vp().max_time_learn, [1] * Globals().vp().max_time_learn]).transpose()
# u=u_all_9
a = 2
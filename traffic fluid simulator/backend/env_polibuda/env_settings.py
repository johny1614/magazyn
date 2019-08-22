import numpy as np
from services.globals import Globals

last_sections = [1, 8, 9, 12, 13, 19, 29, 32]
not_last_sections = [i for i in range(40) if i not in [1, 8, 9, 12, 13, 19, 29, 32]]
stayCoordinates = [(0, 0),
                   (3, 3),
                   (7, 7),
                   (11, 11),
                   (17, 17),
                   (18, 18),
                   (21, 21),
                   (23, 23),
                   (24, 24),
                   (28, 28),
                   (30, 30),
                   (31, 31),
                   (36, 36),
                   (37, 37),
                   (38, 38),
                   (39, 39)
                   ]
freeMovementCoordinates = [(3, 2), (5, 4), (6, 5), (7, 6), (11, 10), (15, 14), (16, 15), (17, 16), (21, 20), (23, 22),
                           (26, 25), (27, 26), (28, 27) , (34, 33), (35, 34), (36, 35)]
sections_of_roads = [
    [0],
    [1],
    [2, 3],
    [4, 5, 6, 7],
    [8],
    [9],
    [10, 11],
    [12],
    [13],
    [14, 15, 16, 17],
    [18],
    [19],
    [20, 21],
    [22, 23],
    [24],
    [25, 26, 27, 28],
    [29],
    [30],
    [31],
    [32],
    [33, 34, 35, 36],
    [37],
    [38],
    [39]
]
source_sections = [0, 18, 24, 30, 31, 37, 38, 39]

x_size = 40


def start_A():
    # it is a red light everywhere A matrix
    A = np.zeros((x_size, x_size))
    for cord in freeMovementCoordinates + stayCoordinates:
        A[cord] = 1
    return A


def get_x():
    x = [x_size * [0]]
    return x


def generate_u(cars_incoming, max_time):
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
# u=u_all_9
a = 2

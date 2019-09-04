import numpy as np

stayCoordinates = [(1, 1), (3, 3)]
freeMovementCoordinates = [(1, 0), (3, 2), (5, 4)]
sections_of_roads = [
    [0, 1], [2, 3], [4, 5]
]
not_last_sections = [0, 1, 2, 3, 4]


def start_A():
    # it is a red light everywhere A matrix
    A = np.zeros((6, 6))
    for cord in freeMovementCoordinates + stayCoordinates:
        A[cord] = 1
    return A


max_time = 1000


def get_x():
    x_size = 6
    x = [x_size * [0]]
    return x


def generate_u(cars_incoming):
    return np.array([[cars_incoming] * max_time, [cars_incoming] * max_time]).transpose()


u_all_2 = np.array([[2] * max_time, [2] * max_time]).transpose()

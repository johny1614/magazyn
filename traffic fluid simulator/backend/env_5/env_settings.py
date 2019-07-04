import numpy as np

stayCoordinates = [(0, 0)]
freeMovementCoordinates = []
sections_of_roads = [
    [0], [1], [2]
]


def start_A():
    # it is a red light everywhere A matrix
    A = np.zeros((3, 3))
    for cord in freeMovementCoordinates + stayCoordinates:
        A[cord] = 1
    return A


max_time = 90


def get_x():
    x_size = 3
    x = [x_size * [0]]
    return x


env_settings_A_storage = [[]] * max_time

u_v1 = np.array([[4, 4, 4, 60, 4, 4, 4, 4, 4, 4, 4, 60, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 60, 4, 4, 4, 4, 4, 4, 4,
                  4, 4, 4, 60, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 60, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 60, 4, 4,
                  4, 4, 4, 4, 60, 4, 4,
                  4, 4, 4, 4, 60, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 60, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                  60, 4, 4, 4, 4, 4, 4,
                  4, 4, 4, 4, 4, 4, 4]]).transpose()

u_all_2 = np.array([[2]*90]).transpose()

u = np.array([[0]*90]).transpose()

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
    for i in range(max_time):
        random_numbers_road_0.append(np.random.random() * x)
        random_numbers_road_1.append(np.random.random() * x)
    return np.array([random_numbers_road_0, random_numbers_road_1]).transpose()
def double_random_u():
    max_x = np.random.random()*15
    random_numbers_road_0 = []
    random_numbers_road_1 = []
    for i in range(max_time):
        random_numbers_road_0.append(np.random.random() * max_x)
        random_numbers_road_1.append(np.random.random() * max_x)
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
u_all_2 = np.array([[2] * max_time, [2] * max_time]).transpose()
#
u_all_4 = np.array([[4] * max_time,[4] * max_time]).transpose()
#
#
u_all_9 = np.array([[9] * max_time, [9] * max_time]).transpose()
#
# u_under_15_random = get_u_under_15_random()
#
# u = np.array([[2] * max_time, [2] * max_time]).transpose()
u = double_random_u()

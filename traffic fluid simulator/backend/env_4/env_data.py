import numpy as np

from Agent import Agent


def get_Agents():
    agent_1_dic = {'all_phases': [[[]], [[(9, 2), (21, 2), (27, 17)],
                                         [(21, 20), (27, 20), (9, 2)],
                                         [(17, 27), (17, 9), (20, 21)]]
                                  ],
                   'actual_phase': [(2, 9), (2, 21), (17, 27)],
                   'actual_phase_duration': 0}
    agent_2_dic = {'all_phases': [[[]], [(11, 12), (11, 30), (26, 18)],
                                  [(5, 12), (5, 18), (11, 30)],
                                  [(26, 18), (26, 30), (5, 12)]],
                   'actual_phase': [(11, 12), (11, 30), (26, 18)],
                   'actual_phase_duration': 0
                   }
    agent_3_dic = {'all_phases': [[[]], [[(14, 33), (14, 23), (23, 24)],
                                         [(8, 14), (8, 15), (14, 33)],
                                         [(23, 24), (23, 33), (8, 15)]]
                                  ],
                   'actual_phase': [(14, 33), (14, 23), (23, 24)],
                   'actual_phase_duration': 0
                   }
    agents = [Agent(agent_1_dic, 3), Agent(agent_2_dic, 3), Agent(agent_3_dic, 3)]
    return agents


def start_A():
    # it is a red light everywhere A matrix
    A = np.zeros((36, 36))
    oneCoordinates = [(1, 0), (2, 1),
                      (4, 3), (5, 4),
                      (7, 6), (8, 7),
                      (10, 9), (11, 10),
                      (13, 12), (14, 13),
                      (16, 15), (17, 16),
                      (19, 18), (20, 19),
                      (22, 21), (23, 22),
                      (25, 24), (26, 25),
                      (28, 27), (29, 28),
                      (31, 30), (32, 31),
                      (34, 33), (35, 34), ]
    for cord in oneCoordinates:
        A[cord] = 1
    return A


# To trzeba bedzie zmieniac tutaj - bo na razie jest dla 1 enva
# Na froncie jest to net3
def hash_(action):
    return tuple([tuple(a) for a in action])

u = np.array([[2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6,
               8, 10, 2, 4, 6, 8, 10],
              [2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6,
               8, 10, 2, 4, 6, 8, 10],
              [1, 3, 5, 7, 9, 1, 3, 5, 7, 9, 1, 3, 5, 7, 9, 1, 3, 5, 7, 9, 1, 3, 5, 7, 9, 1, 3, 5, 7, 9, 1, 3, 5, 7, 9,
               1, 3, 5, 7, 9]]).transpose()

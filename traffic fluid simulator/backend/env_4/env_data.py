import numpy as np

from Agent import Agent

stayCoordinates = [(2, 2),
                   (5, 5),
                   (8, 8),
                   (11, 11),
                   (14, 14),
                   (17, 17),
                   (20, 20),
                   (23, 23),
                   (26, 26),
                   (29, 29),
                   (32, 32),
                   (35, 35)
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
                      (28, 27), (29, 28), (29, 29),
                      (31, 30), (32, 31), (32, 32),
                      (34, 33), (35, 34), (35, 35)]


def get_Agents():
    agent_1_dic = {'all_phases': [[[]], [(9, 2), (21, 2), (27, 17)],
                                         [(21, 20), (27, 20), (9, 2)],
                                         [(27, 17), (9, 17), (21, 20)]]
                                  ,
                   'actual_phase': [[]],
                   # 'actual_phase': [(9, 2), (21, 2), (27, 17)],
                   'actual_phase_duration': 0,
                   'curve_densities': {(9, 2): 0.7, (21, 2): 0.3,
                                       (21, 20): 0.7, (27, 20): 0.3,
                                       (27, 17): 0.7, (9, 17): 0.3}}
    agent_2_dic = {'all_phases': [[[]], [(12, 11), (30, 11), (18, 26)],
                                  [(12, 5), (18, 5), (30, 11)],
                                  [(18, 26), (30, 26), (12, 5)]],
                   'actual_phase': [(12, 11), (30, 11), (18, 26)],
                   'actual_phase_duration': 0,
                   'curve_densities': {(12, 5): 0.7, (18, 5): 0.3,
                                       (30, 11): 0.7, (12, 11): 0.3,
                                       (18, 26): 0.7, (30, 26): 0.3}
                   }
    agent_3_dic = {'all_phases': [[[]], [(33, 14), (15, 14), (24, 23)],
                                         [(24, 8), (15, 8), (33, 14)],
                                         [(24, 23), (33, 23), (15, 8)]
                                  ],
                   'actual_phase': [(33, 14), (15, 14), (24, 23)],
                   'actual_phase_duration': 0,
                   'curve_densities': {(15, 8): 0.7, (24, 8): 0.3,
                                       (33, 14): 0.7, (15, 14): 0.3,
                                       (24, 23): 0.7, (33, 23): 0.3}
                   }
    agents = [Agent(agent_1_dic, 3,1), Agent(agent_2_dic, 3,2), Agent(agent_3_dic, 3,3)]
    return agents


def start_A():
    # it is a red light everywhere A matrix
    A = np.zeros((36, 36))
    for cord in freeMovementCoordinates+stayCoordinates:
        A[cord] = 1
    return A


# To trzeba bedzie zmieniac tutaj - bo na razie jest dla 1 enva
# Na froncie jest to net3
def hash_(action):
    return tuple([tuple(a) for a in action])


curve_densities = 'we'
u = np.array([[2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6,
               8, 10, 2, 4, 6, 8, 10],
              [2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6,
               8, 10, 2, 4, 6, 8, 10],
              [1, 3, 5, 7, 9, 1, 3, 5, 7, 9, 1, 3, 5, 7, 9, 1, 3, 5, 7, 9, 1, 3, 5, 7, 9, 1, 3, 5, 7, 9, 1, 3, 5, 7, 9,
               1, 3, 5, 7, 9]]).transpose()
# x0 = np.array(range(36)).transpose()
x0 = np.zeros(36)

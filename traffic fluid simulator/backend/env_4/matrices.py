import numpy as np
import random

class Agent:
    def __init__(self, dic, min_phase_duration,orange_phase_duration=1):
        self.min_phase_duration = min_phase_duration
        self.all_phases = dic['all_phases']
        self.actual_phase = dic['actual_phase'] # sometimes the pending one
        self.real_phase = dic['actual_phase'] # the one changing A matrix
        self.actual_phase_duration = dic['actual_phase_duration']
        self.possible_actions = self.getLocalActionSpace()
        self.orange_phase_duration=orange_phase_duration
        self.t=0

    def getLocalActionSpace(self):
        waitActions = ['wait']
        light_Actions = [1, 2, 3]
        if (self.actual_phase_duration >= self.min_phase_duration):
            return light_Actions
        return waitActions
    def getRandomAction(self):
        return random.choice(self.getLocalActionSpace())

    def modify_A(self, A):
        if (self.actual_phase_duration == 'wait'):
            return
        for manewr in self.real_phase:
            A[manewr] = 1
    def pass_action(self,action):
        self.t+=1
        if(not action in self.getLocalActionSpace()):
            print('error with passing wrong action',2/0)
        if(action=='wait' and self.actual_phase_duration<self.orange_phase_duration):
            self.actual_phase_duration+=1
            self.actual_phase=self.all_phases[0] # orange one
        elif(action!=self.actual_phase and not action=='wait'): #zmiana swiatla!
            self.actual_phase=action
            self.real_phase=self.all_phases[0] # ORANGE
            self.actual_phase_duration=0
        elif(action==self.actual_phase or action=='wait'):
            self.actual_phase_duration+=1




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


x0 = np.array(range(36)).transpose()
#
# -A-B-
#      -E-F
# -c_D-

T = np.array([[0, 0, 0, 0, 0, 0],  # A
              [1, 1, 0, 0, 0, 0],  # B
              [0, 0, 0, 0, 0, 0],  # C
              [0, 0, 1, 1, 0, 0],  # D
              [0, 1, 0, 1, 0, 0],  # E
              [0, 0, 0, 0, 1, 0]])  # F
#              A  B  C  D  E  F

A_ORANGE = hash_(np.array([[0, 0, 0, 0, 0, 0],  # A
                           [1, 1, 0, 0, 0, 0],  # B
                           [0, 0, 0, 0, 0, 0],  # C
                           [0, 0, 1, 1, 0, 0],  # D
                           [0, 0, 0, 0, 0, 0],  # E
                           [0, 0, 0, 0, 1, 0]]))  # F
#                      A  B  C  D  E  F

UP_A_green = hash_(np.array([[0, 0, 0, 0, 0, 0],  # A
                             [1, 0, 0, 0, 0, 0],  # B
                             [0, 0, 0, 0, 0, 0],  # C
                             [0, 0, 1, 1, 0, 0],  # D
                             [0, 1, 0, 0, 0, 0],  # E
                             [0, 0, 0, 0, 1, 0]]))  # F
#                       A  B  C  D  E  F
DOWN_A_green = hash_(np.array([[0, 0, 0, 0, 0, 0],  # A
                               [1, 1, 0, 0, 0, 0],  # B
                               [0, 0, 0, 0, 0, 0],  # C
                               [0, 0, 1, 0, 0, 0],  # D
                               [0, 0, 0, 1, 0, 0],  # E
                               [0, 0, 0, 0, 1, 0]]))  # F

u = np.array([[2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6,
               8, 10, 2, 4, 6, 8, 10],
              [2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6,
               8, 10, 2, 4, 6, 8, 10],
              [1, 3, 5, 7, 9, 1, 3, 5, 7, 9, 1, 3, 5, 7, 9, 1, 3, 5, 7, 9, 1, 3, 5, 7, 9, 1, 3, 5, 7, 9, 1, 3, 5, 7, 9,
               1, 3, 5, 7, 9]]).transpose()
# turns = [["", "", ""],
#          ["", "", ""],
#          ["right_down_slightly_", "right_up_slightly_", ""], ]

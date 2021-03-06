import numpy as np

# To trzeba bedzie zmieniac tutaj - bo na razie jest dla 1 enva
# Na froncie jest to net3
def hash_(action):
    return tuple([tuple(a) for a in action])

x0 = np.array([1, 2, 3, 4, 5, 6]).transpose()
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
                     [0, 0, 0, 0, 1, 0]]))# F
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
              [1, 3, 5, 7, 9, 1, 3, 5, 7, 9, 1, 3, 5, 7, 9, 1, 3, 5, 7, 9, 1, 3, 5, 7, 9, 1, 3, 5, 7, 9, 1, 3, 5, 7, 9,
               1, 3, 5, 7, 9]]).transpose()
# turns = [["", "", ""],
#          ["", "", ""],
#          ["right_down_slightly_", "right_up_slightly_", ""], ]

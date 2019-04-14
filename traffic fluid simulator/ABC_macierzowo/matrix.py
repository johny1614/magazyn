import numpy as np

# To trzeba bedzie zmieniac tutaj - bo na razie jest dla 1 enva
x0 = np.array([1, 2, 3]).transpose()
#
# -A-
#     -C-
# -B-
#            A  B  C
T = np.array([[0, 0, 0],  # A
              [0, 0, 0],  # B
              [0, 0, 0]])  # C
#            A  B  C
A_a_green = np.array([[0, 0, 0],  # A
                      [0, 1, 0],  # B
                      [1, 0, 0]])  # C
#                      A  B  C
A_b_green = np.array([[1, 0, 0],  # A
                      [0, 0, 0],  # B
                      [0, 1, 0]])  # C

u = np.array([[2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6, 8, 10],
              [1, 3, 5, 7, 9, 1, 3, 5, 7, 9, 1, 3, 5, 7, 9, 1, 3, 5, 7, 9]]).transpose()
# turns = [["", "", ""],
#          ["", "", ""],
#          ["right_down_slightly_", "right_up_slightly_", ""], ]

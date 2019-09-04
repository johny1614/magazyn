import numpy as np

S_0_1 = np.array([
    [0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0]
])
S_2_3 = np.array([
    [0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0]
])
S_matrices = []


def y_ij(x, i, j, p_ij,s_ij, Q_j, N_j):
    return min([p_ij*s_ij * x[i], Q_j, N_j - x[j]])


def get_A(x_history, p,s, escape_i_columns):
    # i to kolumna. j to wiersz. Jedziemy z i do j.
    # Zapis A[j][i] bo pierw wiersz jest
    x = x_history[-1]
    A = np.array([[0.0] * len(x)] * len(x))
    for i in range(len(x)):
        for j in range(len(x)):
            if i in escape_i_columns:
                a = 0
            elif i != j:
                y = y_ij(x_history[0], i=i, j=j, p_ij=p[j][i],s_ij=s[j][i], Q_j=Q, N_j=N)
                a = y / x[i]
            else:
                y_istar = 0
                for j_ in [j__ for j__ in range(len(x)) if j__ != i]:
                    y = y_ij(x_history[0], i=i, j=j_, p_ij=p[j_][i],s_ij=s[j_][i], Q_j=Q, N_j=N)
                    y_istar += y
                if x[i] == 0:
                    a = 10  # chyba obojetne ile
                    print('zeeeeeeero')
                else:
                    a = (x[i] - y_istar) / x[i]
            print(f'i:{i} j:{j} y:{y} a:{a}')
            A[j][i] = a

    return A


Q = 30
N = 30
p = [[0, 0, 0, 0, 0, 0],
     [1, 0, 0, 0, 0, 0],
     [0, 0.25, 0, 0, 0, 0],
     [0, 0, 1, 0, 0, 0],
     [0, 0.75, 0, 0, 0, 0],
     [0, 0, 0, 0, 1, 0]]

x_history = np.array([[9, 4, 3, 0, 1, 5]])
x_history = np.array([[0.00001, 12, 1, 3, 0.000001, 1]])
x_history = np.array([[0.00001, 9, 3, 1, 0.000001, 0.000001]])
x_history = np.array([[0.00001, 0.0001, 2.25, 3, 6.75, 0.000001]])

# y_01 = y_ij(x_history[0], i=0, j=1, p_ij=1, Q_j=Q, N_j=N)
# y_12 = y_ij(x_history[0], i=1, j=2, p_ij=p[2][1], Q_j=Q, N_j=N)
# y_14 = y_ij(x_history[0], i=1, j=4, p_ij=p[4][1], Q_j=Q, N_j=N)
# print(y_12)
# print(y_14)
escape_i_columns = [3, 5]
# A = get_A(x_history, p,S_0_1, escape_i_columns)
for m in range(5):
    A = get_A(x_history, p,S_2_3, escape_i_columns)
    new_x = A.dot(x_history[-1])
    x_history = np.append(x_history, np.array([new_x]), axis=0)
    print(new_x)

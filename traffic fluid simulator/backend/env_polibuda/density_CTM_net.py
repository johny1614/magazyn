import numpy as np


def y_ij(x, i, j, p_ij, Q_j, N_j):
    return min([p_ij * x[i], Q_j, N_j - x[j]])
def get_A(x_history,p,escape_i_columns):
    # i to wiersz, j to kolumna
    x=x_history[-1]
    A=np.array([[0.0]*len(x)]*len(x))
    for i in range(len(x)):
        for j in range(len(x)):
            if i in escape_i_columns:
                a=0
            elif i!=j:
                y = y_ij(x_history[0], i=i, j=j, p_ij=p[j][i], Q_j=Q, N_j=N)
                a = y/x[i]
            else:
                y_istar=0
                for j_ in [j__ for j__ in range(len(x)) if j__!=i]:
                    y = y_ij(x_history[0], i=i, j=j_, p_ij=p[j_][i], Q_j=Q, N_j=N)
                    y_istar+=y
                a=(x[i]-y_istar)/x[i]
            print(f'i:{i} j:{j} y:{y} a:{a}')
            A[j][i]=a


    return A
Q = 10
N = 25
p = [[0, 0,    0, 0, 0, 0],
     [1, 0,    0, 0, 0, 0],
     [0, 0.25, 0, 0, 0, 0],
     [0, 0,    1, 0, 0, 0],
     [0, 0.75, 0, 0, 0, 0],
     [0, 0,    0, 0, 1, 0]]

x_history = np.array([[7, 24, 8, 2, 15, 4]])
# y_01 = y_ij(x_history[0], i=0, j=1, p_ij=1, Q_j=Q, N_j=N)
y_12 = y_ij(x_history[0], i=1, j=2, p_ij=p[2][1], Q_j=Q, N_j=N)
y_14 = y_ij(x_history[0], i=1, j=4, p_ij=p[4][1], Q_j=Q, N_j=N)
print(y_12)
print(y_14)
escape_i_columns=[3,5]
A=get_A(x_history,p,escape_i_columns)
print(A)
print(A.dot(x_history[0]))
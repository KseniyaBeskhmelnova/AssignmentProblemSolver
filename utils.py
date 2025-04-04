import numpy as np
from scipy.optimize import linear_sum_assignment

def create_x(n, x_min, x_max):
    return np.round(np.random.uniform(x_min, x_max, size=n), 2)

def create_c(n, mode):
    c = np.random.randint(1, 101, size=(n, n))
    if mode == "Rows Increasing":
        c = np.sort(c, axis=1)
    elif mode == "Rows Decreasing":
        c = -np.sort(-c, axis=1)
    elif mode == "Cols Increasing":
        c = np.sort(c, axis=0)
    elif mode == "Cols Decreasing":
        c = -np.sort(-c, axis=0)
    return c

def compute_D_matrix(C, chi):
    n = C.shape[0]
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(n - 1, -1, -1):
            if j == n - 1:
                D[i][j] = (1 - chi[i]) * C[i][j]
            else:
                D[i][j] = D[i][j + 1] + (1 - chi[i]) * C[i][j]
    return D

def compute_G_matrix(C, chi):
    n = C.shape[0]
    G = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if j == 0:
                G[i, j] = (1 - chi[i]) * C[i, j]
            else:
                G[i, j] = G[i, j - 1] + (1 - chi[i]) * C[i, j]
    return G

def hungarian_algorithm(D):
    D_T = D.T
    cost_D_T = np.max(D_T) - D_T
    row_ind, col_ind = linear_sum_assignment(cost_D_T)
    return col_ind, D_T[row_ind, col_ind].sum()

def greedy_algorithm(D):
    D_T = D.T
    col_ind = []
    assigned = set()
    for j in range(D_T.shape[0]):
        best_i = -1
        best_value = -np.inf
        for i in range(D_T.shape[1]):
            if i not in assigned and D_T[j][i] > best_value:
                best_value = D_T[j][i]
                best_i = i
        col_ind.append(best_i)
        assigned.add(best_i)
    total_value = sum(D_T[j, col_ind[j]] for j in range(len(col_ind)))
    return col_ind, total_value

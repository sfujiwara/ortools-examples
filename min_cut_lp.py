from ortools.linear_solver import pywraplp
import numpy as np
from scipy.spatial import distance_matrix

np.random.seed(42)

xs = np.random.uniform(size=[20, 2])
dmat = distance_matrix(xs, xs)

n_nodes = len(dmat)

solver = pywraplp.Solver('mincut', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

# min_xy sum_ij [w_ij y_ij]
# s.t.   y_ij - x_i + x_j >= 0
#        sum_i x_i = n

# x_i_j: 0-1 integer variables
x = {}
for i in range(1):
    for j in range(n_nodes):
        x[i, j] = solver.BoolVar('x_{}_{}'.format(i, j))
        # x[i, j] = solver.NumVar(lb=0, ub=1, name='x_{}_{}'.format(i, j))

# y_i_j: continuous variables in [0, 1]
y = {}
for i in range(n_nodes):
    for j in range(n_nodes):
        # y[i, j] = solver.NumVar(lb=0., ub=np.inf, name='y_{}_{}'.format(i, j))
        y[i, j] = solver.BoolVar(name='y_{}_{}'.format(i, j))

# Objective
objective = 0
for i in range(n_nodes):
    for j in range(n_nodes):
        objective += y[i, j] * dmat[i, j]

# Constraints
for i in range(1):
    for j in range(n_nodes):
        for k in range(n_nodes):
            solver.Add(y[j, k] - x[i, j] + x[i, k] >= 0)

for i in range(1):
    sum_x = 0
    for j in range(n_nodes):
        sum_x += x[i, j]
    solver.Add(sum_x == 240)
    # solver.Add(sum_x <= n_nodes-1)

solver.Add(x[0, 1] == 1)
solver.Add(x[0, 2] == 0)
solver.Add(x[0, 3] == 1)
solver.Add(x[0, 4] == 0)

solver.Minimize(objective)
print('solve')
result = solver.Solve()

print('objective value: {}'.format(solver.Objective().Value()))
print(solver.wall_time() / 1000)
for i in range(1):
    for j in range(n_nodes):
        print('{}: {}'.format(x[i, j].name(), x[i, j].solution_value()))

# for i in range(n_nodes):
#     for j in range(n_nodes):
#         print('{}: {}'.format(y[i, j].name(), y[i, j].solution_value()))

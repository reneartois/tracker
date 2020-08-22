"""
config file for KalmanFilter_Custom
Depending on X0, the corresponding subset of matrices are used.
Ex X0= [1, 0]', nz=1. H[nz, nx] = (1,2)
"""
# dt
dt = 0.1

# state transition matrix, nx * nx
F = [[1, dt, 0, 0],
     [0, 1, 0, 0],
     [0, 0, 1, dt],
     [0, 0, 0, 1]]

# control input transaction matrix, nx * nu
B = None

# control inputs,
u = None

#Observation matrix, nz * nx
H = [[1, 0, 0, 0],
     [0, 0, 1, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]]


# kalman filter gain, nx * nz
# weigth of measurement, (1- K) is weight of estimate
K0 = [[0.2, 0, 0, 0],
     [0, 0.2, 0, 0],
     [0, 0, 0.2, 0],
     [0, 0, 0, 0.2]]

# measurement uncertainty, std dev, nz * nz
R = [[10, 0, 0, 0],
     [0, 10, 0, 0],
     [0, 0, 10, 0],
     [0, 0, 0, 10]]


# process noise uncertainty, std dev, nx * nx
# 0 = no process noise. small q: lag error. high q: filter follows measurements
Q = [[0.1, 0, 0, 0],
     [0, 0.1, 0, 0],
     [0, 0, 0.1, 0],
     [0, 0, 0, 0.1]]

# state estimation uncertainty, std dev, nx * nx
P0 = [[3, 0, 0, 0],
     [0, 3, 0, 0],
     [0, 0, 3, 0],
     [0, 0, 0, 3]]

# Options
PRINT_VALUES = True
# initial values
X0 = [0, 1, 0, 0]
nz= 2

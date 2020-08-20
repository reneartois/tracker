"""
config file for KalmanFilter_Custom
"""
# dt

dt = 1

# state transition matrix, nx * nx
F = [[1, dt],
     [0, 1]]
F = [[1]]
F = [[1, 0, dt, 0],
     [0, 1, 0, dt],
     [0, 0, 1, 0],
     [0, 0, 0, 1]]
F = [[1, dt, 0, 0],
     [0, 1, 0, 0],
     [0, 0, 1, dt],
     [0, 0, 0, 1]]

# control input transaction matrix, nx * nu
B = None

# control inputs,
u = None

#Observation matrix, nz * nx
H = [[1, 0],
     [0, 1]]
H = [1]
H = [[1, 0, 0, 0],
     [0, 0, 1, 0]]


# kalman filter gain, nx * nz
# weigth of measurement, (1- K) is weight of estimate
K0 = [[1, 0],
     [0, 1]]
K0 = [[0.8]]
K0 = [[1, 0],
     [0, 0],
     [0, 1],
     [0, 0]]

# measurement uncertainty, std dev, nz * nz
R = [0.1]
R = [[0.1, 0],
     [0, 0.1]]
Rr = [[0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]]


# process noise uncertainty, std dev, nx * nx
# 0 = no process noise. small q: lag error. high q: filter follows measurements
q0 = 0.1
Q = [[0, 0, 0, 0],
     [0, 0.1, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0.1]]

# state estimation uncertainty, std dev, nx * nx
P0 = [100]
P0 = [[0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]]

# Options
PRINT_VALUES = True
# initial values
X0 = [0, 1, 0, 0]

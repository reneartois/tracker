"""
Notations from:
Understanding the Basis of the Kalman Filter via a Simple and Intuitive Derivation, R. Faragher.
Signal Processing Magazine, IEEE , vol.29, no.5, pp.128-132, Sept. 2012 doi: 10.1109/MSP.2012.2203621
"""
# dt
dt = 0.1
# state transition matrix, nx * nx
F = [[1, dt],
     [0, 1]]
# control input transaction matrix, nx * nu
B = None
# control inputs,
u = None
#Observation matrix, nz * nx
#H = [1, 1]
H = [[1, 0],
     [0, 1]]
# kalman filter gain, nx * nz
K = [[1, 0],
     [0, 1]]
# measurement uncertainty, std dev, nz * nz
r0 = [1, 1]
# process noise uncertainty, std dev, nx * nx
# 0 = no process noise. small q: lag error. high q: filter follows measurements
# if uncorrelated, estimator creates eye matrix from q0_vector, otherwize, specify q0_matrix
Q_UNCORRELATED= False
q0_v = [0.7, 0.7]
q0_m = [[0.8, 0.8],
        [0.8, 0.8]]
# state estimation uncertainty, std dev, xz * nx
p0 = [0.1, 0.5]

# Options
PRINT_VALUES = False
# initial values
X0 = [0, 10]


#pykalman?

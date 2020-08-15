"""
Notations from:
Understanding the Basis of the Kalman Filter via a Simple and Intuitive Derivation, R. Faragher.
Signal Processing Magazine, IEEE , vol.29, no.5, pp.128-132, Sept. 2012 doi: 10.1109/MSP.2012.2203621

system states
[x y v theta]'

estimated state:
[x y vx vy]'

"""
# dt
dt = 0.1
# state transition matrix
F = [[1, dt],
     [0, 1]]
# control input transaction matrix
B = None
# control inputs
u = None
#Observation matrix
#H = [1, 1]
H = [[1, 0],
     [0, 1]]
# kalman filter gain
K = [0.5, 0.5]
# measurement uncertainty, std dev
r0 = [[1, 1]]
# process noise uncertainty, std dev.
    # 0 = no process noise
    # independent. small q: lag error. high q: filter follows measurements
    # if uncorrelated, estimator creates eye matrix from q0_vector
    # otherwize, specify q0_matrix
Q_UNCORRELATED= True
q0_v = [0.1, 0.1]
q0_m = [[0.5, 0.5], [0.5, 0.5]]
# state estimation uncertainty, std dev
p0 = [0.1, 0.1]

# Options
PRINT_VALUES = False
# initial values
X0 = [0, 0]


#pykalman?

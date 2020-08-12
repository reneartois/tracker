# model
#dx = v = dx dt
#dv = 0
dt = 5
A = [[1]]
B = None
u = None

# initial values
X0 = [[60]]

# kalman filter gain
# K = [0.9, 0]
K = [0.9]

# measurements
TRUE_VALUE = 50
MEASUREMENTS = [[48.54, 47.11, 55.01, 55.15, 49.89,
                40.85, 46.72, 50.05, 51.27, 49.95]]

# estimate uncertainty, std dev
p0 = [15]

# measurement uncertainty, std dev
r0 = [5]

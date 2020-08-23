"""
config file for KalmanFilter and corresponding Gui app.

Kalman filter:
Depending on X0, the corresponding subset of matrices are used.
Ex X0= [1, 0]' and nz=1: H[nz, nx].shape = (1,2)

GUI:
mainly display settings
"""
# kalman filter---------------------------------------------
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
# continously updated
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
qv = 1
Qv = [[0, 0, 0, 0],
     [0, qv, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, qv]]

# state estimation uncertainty, std dev, nx * nx
# continously updated
P0 = [[3, 0, 0, 0],
     [0, 3, 0, 0],
     [0, 0, 3, 0],
     [0, 0, 0, 3]]

# Options
PRINT_VALUES = True
# initial values
#X0 = [0, 1, 0, 0]
#nz= 2

# GUI app --------------------------------------------------
master_title = "Estimator"
master_width = 1000
master_heigth = 600

# canvas
show_true_values = True
show_measured_values = True
show_est_values = True
canvas_oval_delta = 3
n_stored_values = 40
canvas_bg_color = "black"
canvas_true_val_color = "red"
canvas_measurement_color = "blue"
canvas_estimate_color = "green"

# frames
canvas_width = 1000
canvas_height =400
main_frame_heigth = 200
main_frame_width=350

# display frame
display_padx= 40
display_pady=5

#noise
sigma = 30
mu = 0

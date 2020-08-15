import numpy as np
from scipy.integrate import odeint
from matplotlib import pyplot as plt
import math

class Vehicle():
    def __init__(self):
        """
        https://se.mathworks.com/help/control/getstart/estimating-states-of-time-varying-systems-using-kalman-filters.html
        Skipped model
        """
        self.N_POINTS = 100
        self.t = np.linspace(0, 1000, self.N_POINTS)

    def generate_trajectory_1(self):
        self.N_STATES = 2
        self.X = np.zeros((self.N_STATES, self.N_POINTS))
        v = 10
        dt = 0.1
        seq1 = self.N_POINTS / 3
        seq2 = 2 * self.N_POINTS / 3
        for i in range(1, self.N_POINTS):
            if i > seq1:
                v = 25
            if i > seq2:
                v = -40
            self.X[0, i] = self.X[0, i - 1] + dt * v
            self.X[1, i] = v
        return self.X

    def plot_trajectory_1(self, x_est, x_true):
        n_states = self.N_STATES
        n_measurements = self.N_POINTS

        t = np.linspace(1, n_measurements, n_measurements)
        x_ = x_est[0, :]
        v_ = x_est[1, :]
        x = x_true[0, :]
        v = x_true[1, :]

        fig, (ax1, ax2) = plt.subplots(2)
        ax1.plot(t, x, t, x_)
        ax1.set_title("x-position")
        ax2.plot(t, v, t, v_)
        ax2.set_title("speed")
        plt.show()


    def generate_trajectory_2(self):
        self.u = np.zeros((self.N_STATES, self.N_POINTS))
        self.N_STATES = 2
        dt = 0.1
        v0 = 200
        omega = 10
        theta = 0
        acc = 2
        #self.t = np.linspace(0, (self.N_POINTS-1) * dt, self.N_POINTS)
        self.X = np.zeros((self.N_STATES, self.N_POINTS))

        # constant velocity
        seq1 = math.floor(self.N_POINTS/3)
        for s in range(1, seq1):
            self.X[2, s] = v0
            self.X[0, s] = self.X[0, s-1] + v0 * dt
            #print(s)

        # constant turn
        omega_rad = np.radians(omega)
        theta_rad = np.radians(theta)
        seq2 = math.floor(2 * self.N_POINTS/3)
        for s in range(seq1, seq2):
            theta_rad += omega_rad*dt
            vx = v0 * np.cos(theta_rad)
            vy = v0 * np.sin(theta_rad)
            self.X[0, s] = self.X[0, s-1] + vx * dt
            self.X[1, s] = self.X[1, s-1] + vy * dt
            self.X[2, s] = vx
            self.X[3, s] = vy

        # constant acceleration
        for s in range(seq2, self.N_POINTS):
            v0 += dt * acc
            vx = v0 * np.cos(theta_rad)
            vy = v0 * np.sin(theta_rad)
            self.X[0, s] = self.X[0, s-1] + vx * dt
            self.X[1, s] = self.X[1, s-1] + vy * dt
            self.X[2, s] = vx
            self.X[3, s] = vy
        #plt.plot(self.X[0, :], self.X[1, :])
        #plt.show()
        return self.X

    def generate_measurements(self):
        mu = 0
        sigma = 3
        return self.X + np.random.randn(self.X.shape[0], self.X.shape[1]) * sigma + mu

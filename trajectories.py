import numpy as np
import math
import matplotlib.pyplot as plt
import tkinter

class Trajectory:
    """
    Generate trajectory for KF
    NOT USED
    """
    def __init__(self, dt, n_points, X0):
        """
        """

        self.dt = dt
        self.N_STATES = len(X0)
        self.N_POINTS = n_points
        self.X = np.zeros((9, self.N_POINTS))
        self.X[0: self.N_STATES, 0] = X0


    def generate_trajectory(self):
        x_ind = [0, 3, 6]
        v_ind = [1, 4, 7]
        a_ind = [2, 5, 8]
        dt = self.dt
        for i in range(1, self.N_POINTS):
            self.X[0, i] = self.X[0, i-1] + self.X[1, i-1] * dt + 0.5 * self.X[2, i-1] * dt**2
            self.X[1, i] = self.X[1, i-1] + self.X[2, i-1] * dt
            self.X[2, i] = self.X[2, i-1]
            self.X[3, i] = self.X[3, i-1] + self.X[4, i-1] * dt + 0.5 * self.X[5, i-1] * dt**2
            self.X[4, i] = self.X[4, i-1] + self.X[5, i-1] * dt
            self.X[5, i] = self.X[5, i-1]
            self.X[6, i] = self.X[6, i-1] + self.X[7, i-1] * dt + 0.5 * self.X[8, i-1] * dt**2
            self.X[7, i] = self.X[7, i-1] + self.X[8, i-1] * dt
            self.X[8, i] = self.X[8, i-1]
        self.X = self.X[0: self.N_STATES, :]
        return self.X


    def generate_trajectory_2D_constvel_constturn_constacc(self):
        dt = self.dt
        v0 = 2
        theta = 0
        omega = 2
        acc = 2

        # constant velocity
        seq1 = math.floor(self.N_POINTS/3)
        for i in range(1, seq1):
            self.X[0, i] = self.X[0, i-1] + v0 * dt
            self.X[1, i] = v0

        # constant turn
        omega_rad = np.radians(omega)
        theta_rad = np.radians(theta)
        seq2 = math.floor(2 * self.N_POINTS/3)
        vx = v0 * np.cos(theta_rad)
        vy = v0 * np.sin(theta_rad)
        for i in range(seq1, seq2):
            theta_rad += omega_rad * dt
            self.X[0, i] = self.X[0, i-1] + vx * dt
            self.X[1, i] = vx
            self.X[3, i] = self.X[3, i-1] + vy * dt
            self.X[4, i] = vy
            vx = v0 * np.cos(theta_rad)
            vy = v0 * np.sin(theta_rad)

        accx = np.cos(theta_rad)
        accy = np.sin(theta_rad)
        # constant acceleration
        for i in range(seq2, self.N_POINTS):
            self.X[0, i] = self.X[0, i-1] + vx * dt + 0.5 * accx **2
            self.X[1, i] = vx
            self.X[2, i] = accx
            self.X[3, i] = self.X[3, i-1] + vy * dt + 0.5 * accy **2
            self.X[4, i] = vy
            self.X[5, i] = accy
            v0 += dt * acc
            vx = v0 * np.cos(theta_rad)
            vy = v0 * np.sin(theta_rad)

        self.X = self.X[0: self.N_STATES, :]
        return self.X


    def generate_measurements(self, sigma, mu=0):
        r =self.X + np.random.randn(self.X.shape[0], self.X.shape[1]) * self.sigma + self.mu
        return r

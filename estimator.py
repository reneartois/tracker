import config
import numpy as np
import matplotlib.pyplot as plt

class Estimator():
    """Estimate state"""
    i = 0

    def __init__(self):
        self.X_estimate = config.X0
        self.A = np.matrix(config.A)
        self.dt = config.dt
        self.K = np.matrix(config.K)
        self.last_measurement = self.X_estimate
        self.p = np.matrix(config.p0)**2
        self.r = np.matrix(config.r0)**2
        self.B = None
        if config.B is not None:
            self.B = np.matrix(config.B)
        self.u = None
        if config.u is not None:
            self.u = np.matrix(config.u)
        self.MEASUREMENTS = np.matrix(config.MEASUREMENTS)
        #print(self.MEASUREMENTS)
        self.N_MEASUREMENTS = self.MEASUREMENTS.shape[1]
        X_EST = np.zeros((self.A.shape[0], self.N_MEASUREMENTS))
        self.i = 0

    def estimate_current_state(self):
        """State update equation"""
        z = self.last_measurement
        x_hat = (1 - self.K).dot(self.X_estimate) + self.K.dot(z)
        self.X_estimate = x_hat
        print(f"current estimate: {self.X_estimate}")


    def predict_next_state(self):
        """Prediction Equation"""
        x_hat = self.A.dot(self.X_estimate)
        if self.B is not None and self.u is not None:
            x_hat += self.B.dot(self.u)
        self.X_estimate = x_hat
        print(f"predicted next: {self.X_estimate}")


    def update_kalman_gain(self):
        """Kalman Gain update"""
        self.K = self.p / (self.p + self.r)
        print(f"kalman gain: {self.K}")


    def update_estimate_uncertainty(self):
        """Covariance update"""
        self.p = (1 - self.K).dot(self.p)
        print(f"cov: {self.p}")


    def increment_iteration(self):
        self.i += 1


    def covariance_extrapolation(self):
        """Covariance extrapolation"""
        self.p = self.p
        print(f"cov: {self.p}")


    def make_measurement(self):
        self.last_measurement = self.MEASUREMENTS[:, self.i]
        print(f"measurement: {self.last_measurement}")


    def estimated_state(self):
        return self.X_estimate





    def example_plot2(self):
        x = np.linspace(0,10,50)
        y = x**2

        plt.ion()
        fig = plt.figure()
        ax = fig.add_subplot(111)

        l,  = plt.plot(x[0], y[0], "r-")

        for i in range(len(x)):
            l.set_data(y[:i], x[:i])
            ax.relim()
            ax.autoscale_view(True, True, True)
            plt.draw()
            plt.pause(0.1)

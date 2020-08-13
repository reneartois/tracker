import config
import numpy as np

class Estimator():
    """Estimate state"""

    def __init__(self):
        # state vector
        self.X_estimate = np.transpose(np.matrix(config.X0))

        # state transition matrix
        self.F = np.matrix(config.F)

        # control input transaction matrix
        self.G = None
        if config.G is not None:
            self.G = np.matrix(config.G)

        # control matrix
        self.u = None
        if config.u is not None:
            self.u = np.matrix(config.u)

        # kalman gain
        self.K = np.matrix(config.K)

        # measurement uncertainty, covariance matrix
        self.R = np.diag(config.r0)**2

        # process noise uncertainty, cov matrix
        self.Q = np.diag(config.q0)**2

        # state estimation uncertainty cov matrix
        self.P = np.diag(config.p0)**2

        self.last_measurement = self.X_estimate
        self.I = np.eye(self.K.shape[1])



        # observation matrix
        if config.ALL_STATES_MEASUREABLE:
            self.H = np.eye(self.F.shape[0])
        else:
            self.H = np.eye(self.F.shape[0])

        self.MEASUREMENTS = np.matrix(config.MEASUREMENTS)
        self.N_MEASUREMENTS = self.MEASUREMENTS.shape[1]
        self.X_estimate_array = np.zeros((self.F.shape[0], self.N_MEASUREMENTS))
        self.i = 0
        self.print_values = config.PRINT_VALUES
        self.dt = config.dt

    # PREDICTION EQUATIONS
    def predict_next_state(self):
        """state extrapolation equation"""
        x_hat = self.F.dot(self.X_estimate)
        if self.G is not None and self.u is not None:
            x_hat += self.G.dot(self.u)
        self.X_estimate = x_hat
        self.print(f"predicted next: {self.X_estimate}")


    def covariance_extrapolation(self):
        """Covariance extrapolation"""
        self.P = self.F.dot(self.P).dot(np.transpose(self.F)) + self.Q
        self.print(f"cov: {self.P}")


    # ESTIMATION EQUATIONS
    def estimate_current_state(self):
        """State update equation"""
        z = self.last_measurement
        e = z - self.H.dot(self.X_estimate)
        self.X_estimate = self.X_estimate + self.K.dot(e)
        self.print(f"current estimate: {self.X_estimate}")
        self.X_estimate_array[:, self.i] = self.X_estimate


    def update_estimate_uncertainty(self):
        """Covariance update equation"""
        i_minus_kh = self.I - self.K.dot(self.H)
        i_minus_kh_t = np.transpose(i_minus_kh)
        krk = self.K.dot(self.R).dot(np.transpose(self.K))
        self.P = i_minus_kh.dot(self.P).dot(i_minus_kh_t) + krk
        self.print(f"cov: {self.P}")


    def update_kalman_gain(self):
        """Kalman Gain update"""
        hph_r = self.H.dot(self.P).dot(np.transpose(self.H)) + self.R
        hph_r = np.linalg.inv(hph_r)
        self.K = self.P.dot(np.transpose(self.H)).dot(hph_r)
        self.print(f"kalman gain: {self.K}")


    def increment_iteration(self):
        self.i += 1





    def make_measurement(self):
        """ measurement equation"""
        # z = H*x + noise
        # H -observation matrix
        self.last_measurement = self.MEASUREMENTS[:, self.i]
        self.print(f"measurement: {self.last_measurement}")


    def estimated_state(self):
        return self.X_estimate


    def print(self, str):
        if self.print_values:
            print(str)

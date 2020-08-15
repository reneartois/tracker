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
        self.B = None
        if config.B is not None:
            self.B = np.matrix(config.B)
        # control matrix
        self.u = None
        if config.u is not None:
            self.u = np.matrix(config.u)
        # observation matrix
        self.H = np.matrix(config.H)
        # kalman gain
        self.K = np.matrix(config.K)
        # measurement uncertainty, covariance matrix
        self.R = np.diag(config.r0)**2
        # process noise uncertainty, cov matrix
        if config.Q_UNCORRELATED:
            self.Q = np.diag(config.q0_v)**2
        else:
            self.Q = np.matrix(config.q0_m)**2
        # state estimation uncertainty cov matrix
        self.P = np.diag(config.p0)**2

        self.last_measurement = self.X_estimate
        self.I = np.eye(self.K.shape[1])
        self.print_values = config.PRINT_VALUES

    # PREDICTION EQUATIONS
    def predict_next_state(self):
        """state extrapolation"""
        x_hat = self.F.dot(self.X_estimate)
        if self.B is not None and self.u is not None:
            x_hat += self.B.dot(self.u)
        self.X_estimate = x_hat
        self.print(f"predicted next: {self.X_estimate}")


    def covariance_extrapolation(self):
        """Process noise covariance extrapolation"""
        self.P = self.F.dot(self.P).dot(np.transpose(self.F)) + self.Q
        self.print(f"cov: {self.P}")


    # ESTIMATION EQUATIONS
    def estimate_current_state(self):
        """State update"""
        x = self.X_estimate
        z = self.last_measurement
        e = z - self.H.dot(x)
        self.X_estimate = x + self.K.dot(e)
        self.print(f"current estimate: {self.X_estimate}")
        #print(self.X_estimate.shape)
        return self.X_estimate


    def update_estimate_uncertainty(self):
        """Covariance update"""
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


    def test_estimator():

        pass


    def make_measurement(self, y):
        """ measurement equation
            y(measured_states, 1)
        """
        # z = H*x + noise
        # C -observation matrix
        self.last_measurement = self.H.dot(y)
        self.print(f"measurement: {self.last_measurement}")


    def estimated_state(self):
        return self.X_estimate


    def print(self, str):
        if self.print_values:
            print(str)
